##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: November 20, 2020
##   | |    | | \ \    ---------------------------------
##   |_|    |_|  \_\   https://github.com/pedrorrivero
##

from numpy import uint32, uint64
from qiskit import (
    BasicAer,
    ClassicalRegister,
    QuantumCircuit,
    QuantumRegister,
    execute,
)
from qiskit.providers.ibmq import least_busy
from randomgen import UserBitGenerator


###############################################################################
## BIT CACHE
###############################################################################
class BitCache:
    def __init__(self):
        self._cache = ""
        self.size = 0

    ############################# STATIC METHODS #############################
    @staticmethod
    def isbitstring(bitstring: str) -> bool:
        if not isinstance(bitstring, str):
            raise TypeError(f"Invalid bitstring type '{type(bitstring)}'")
        b = {"0", "1"}
        s = set(bitstring)
        return s.issubset(b)

    ############################# PUBLIC METHODS #############################
    def flush(self) -> str:
        bitstring = self._cache
        self._cache = ""
        self.size = 0
        return bitstring

    def get(self, n: int) -> str:
        bitstring = self._cache[:n]
        self._cache = self._cache[n:]
        self.size -= n if n < self.size else self.size
        return bitstring

    def put(self, bitstring: str) -> bool:
        if not BitCache.isbitstring(bitstring):
            raise ValueError(f"Invalid bitstring value '{bitstring}'")
        self._cache += bitstring
        self.size += len(bitstring)
        return True

    ############################ PUBLIC PROPERTIES ############################
    @property
    def state(self) -> dict:
        return {"size": self.size}


###############################################################################
## QISKIT BIT GENERATOR
###############################################################################
class QiskitBitGenerator:
    def __init__(self, provider=None, backend=None):
        if provider and not backend:
            backend = QiskitBitGenerator.get_best_backend(provider)
        if not backend:
            backend = BasicAer.get_backend("qasm_simulator")
        self._backend = backend
        self._provider = backend.provider
        self._bitcache = BitCache()

    ############################# STATIC METHODS #############################
    @staticmethod
    def get_best_backend(provider):
        def filters(b):
            config = b.configuration()
            return config.memory and not config.simulator

        backends = provider.backends(filters=filters)
        return least_busy(backends) if backends else None

    ############################# PUBLIC METHODS #############################
    def get_bitstring(self, n: int) -> str:
        while self._bitcache.size < n:
            self._fetch_random_bits()
        return self._bitcache.get(n)

    ############################# PRIVATE METHODS #############################
    def _fetch_random_bits(self) -> bool:
        circuits = [self._circuit] * self._get_experiments()
        job = execute(circuits, self._backend, shots=self._get_shots())
        result = job.result()
        measurements = self._parse_results(result)
        for m in measurements:
            self._bitcache.put(m)
        return True

    def _get_experiments(self) -> int:
        config = self._config
        return config["max_experiments"] if config["max_experiments"] else 1

    def _get_shots(self) -> int:
        config = self._config
        return config["max_shots"] if config["memory"] else 1

    def _parse_results(self, result):
        config = self._config
        if config["memory"]:
            raise NotImplementedError(
                "Strategy for Result.get_memory() not implemented \
                (see qiskit-terra #5415 on github)"
            )
        else:
            counts = result.get_counts()
            counts = [counts] if type(counts) != list else counts
            measurements = []
            for c in counts:
                m = [k for k, v in c.items() if v == 1][0]
                measurements.append(m)
        return measurements

    ############################ PUBLIC PROPERTIES ############################
    @property
    def state(self):
        return {"backend": self._config, "bitcache": self._bitcache.state}

    ########################### PRIVATE PROPERTIES ###########################
    @property
    def _circuit(self) -> QuantumCircuit:
        config = self._config
        qr = QuantumRegister(config["n_qubits"])
        cr = ClassicalRegister(config["n_qubits"])
        circuit = QuantumCircuit(qr, cr)
        circuit.h(qr)
        circuit.measure(qr, cr)
        return circuit

    @property
    def _config(self):
        config = {
            "backend_name": "",
            "credits_required": False,
            "local": True,
            "max_experiments": None,
            "max_shots": None,
            "memory": False,
            "n_qubits": None,
            "simulator": True,
        }
        backend_config = self._backend.configuration().to_dict()
        keys = backend_config.keys()
        for k in config.keys():
            if k in keys:
                config[k] = backend_config[k]
        config["memory"] = False  # Bug(github): qiskit-terra #5415
        return config

    ############################# NUMPY INTERFACE #############################
    def random_raw(self) -> uint64:
        """Generate the next "raw" value, which is 64 bits"""
        bitstring = self.get_bitstring(64)
        random = int(bitstring, 2)
        return uint64(random)

    @property
    def next_64(self):
        """
        Return a callable that accepts a single input and returns a numpy
        64-bit unsigned int. The input is usually a void pointer that is cast
        to a struct that contains the RNGs state. When wiring a bit generator
        in Python, it is simpler to use a closure than to wrap the state in an
        array, pass it's address as a ctypes void pointer, and then to get the
        pointer in the function.
        """

        def _next_64(void_p):
            return self.random_raw()

        return _next_64

    @property
    def next_32(self):
        """
        Return a callable that accepts a single input. This is identical to
        ``next_64`` except that it returns a numpy 32-bit unsigned int.
        """

        def _next_32(void_p):
            bitstring = self.get_bitstring(32)
            random = int(bitstring, 2)
            return uint32(random)

        return _next_32

    @property
    def state_getter(self):
        def f():
            return self.state

        return f

    @property
    def state_setter(self):
        def f(value):
            keys = value.keys()
            if "backend" in keys:
                self._backend = value["backend"]
            if "flush_bitcache" in keys:
                if value["flush_bitcache"]:
                    self._bitcache.flush()

        return f


###############################################################################
## QISKIT BIT GENERATOR WRAPPER FOR NUMPY
###############################################################################
def QiskitNumpyBitGenerator(provider=None, backend=None, bitgen=None):
    if not bitgen:
        bitgen = QiskitBitGenerator(provider=provider, backend=backend)
    return UserBitGenerator(
        bitgen.next_64,
        64,
        next_32=bitgen.next_32,
        state_getter=bitgen.state_getter,
        state_setter=bitgen.state_setter,
    )
