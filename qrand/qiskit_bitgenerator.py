##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: November 21, 2020
##   | |    | | \ \    ---------------------------------
##   |_|    |_|  \_\   https://github.com/pedrorrivero
##

from typing import Any, Callable, Dict, KeysView, List, Optional, Set

from numpy import uint32, uint64
from qiskit import (
    BasicAer,
    ClassicalRegister,
    QuantumCircuit,
    QuantumRegister,
    execute,
)
from qiskit.providers import Backend, Job, Provider
from qiskit.providers.ibmq import least_busy
from qiskit.providers.models import BackendConfiguration
from qiskit.result import Counts, Result
from randomgen import UserBitGenerator


###############################################################################
## BIT CACHE
###############################################################################
class BitCache:
    def __init__(self) -> None:
        self._cache: str = ""
        self.size: int = 0

    ############################# STATIC METHODS #############################
    @staticmethod
    def isbitstring(bitstring: str) -> bool:
        if not isinstance(bitstring, str):
            raise TypeError(f"Invalid bitstring type '{type(bitstring)}'")
        b: Set[str] = {"0", "1"}
        s: Set[str] = set(bitstring)
        return s.issubset(b)

    ############################# PUBLIC METHODS #############################
    def flush(self) -> str:
        bitstring: str = self._cache
        self._cache = ""
        self.size = 0
        return bitstring

    def get(self, n: int) -> str:
        bitstring: str = self._cache[:n]
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
    def state(self) -> Dict[str, int]:
        return {"size": self.size}


###############################################################################
## QISKIT BIT GENERATOR
###############################################################################
class QiskitBitGenerator:
    def __init__(
        self,
        provider: Optional[Provider] = None,
        backend: Optional[Backend] = None,
    ) -> None:
        if provider and not backend:
            backend = QiskitBitGenerator.get_best_backend(provider)
        if not backend:
            backend = BasicAer.get_backend("qasm_simulator")
        self._backend: Backend = backend
        self._provider: Provider = backend.provider
        self._bitcache: BitCache = BitCache()

    ############################# STATIC METHODS #############################
    @staticmethod
    def get_best_backend(provider: Provider) -> Optional[Backend]:
        def filters(b: Backend) -> bool:
            config: BackendConfiguration = b.configuration()
            return config.memory and not config.simulator

        backends: List[Backend] = provider.backends(filters=filters)
        return least_busy(backends) if backends else None

    ############################# PUBLIC METHODS #############################
    def get_bitstring(self, n: int) -> str:
        while self._bitcache.size < n:
            self._fetch_random_bits()
        return self._bitcache.get(n)

    ############################# PRIVATE METHODS #############################
    def _fetch_random_bits(self) -> bool:
        circuits: List[QuantumCircuit] = [
            self._circuit
        ] * self._get_experiments()
        job: Job = execute(circuits, self._backend, shots=self._get_shots())
        result: Result = job.result()
        measurements: List[str] = self._parse_result(result)
        for m in measurements:
            self._bitcache.put(m)
        return True

    def _get_experiments(self) -> int:
        config: Dict[str, Any] = self._config
        return config["max_experiments"] if config["max_experiments"] else 1

    def _get_shots(self) -> int:
        config: Dict[str, Any] = self._config
        return config["max_shots"] if config["memory"] else 1

    def _parse_result(self, result: Result) -> List[str]:
        config: Dict[str, Any] = self._config
        if config["memory"]:
            raise NotImplementedError(
                "Strategy for Result.get_memory() not implemented \
                (see qiskit-terra #5415 on github)"
            )
        else:
            cts = result.get_counts()
            counts: List[Counts] = [cts] if type(cts) != list else cts
            measurements: List[str] = []
            for c in counts:
                m: str = [k for k, v in c.items() if v == 1][0]
                measurements.append(m)
        return measurements

    ############################ PUBLIC PROPERTIES ############################
    @property
    def state(self) -> Dict[str, Any]:
        return {"backend": self._config, "bitcache": self._bitcache.state}

    ########################### PRIVATE PROPERTIES ###########################
    @property
    def _circuit(self) -> QuantumCircuit:
        config: Dict[str, Any] = self._config
        qr: QuantumRegister = QuantumRegister(config["n_qubits"])
        cr: ClassicalRegister = ClassicalRegister(config["n_qubits"])
        circuit: QuantumCircuit = QuantumCircuit(qr, cr)
        circuit.h(qr)
        circuit.measure(qr, cr)
        return circuit

    @property
    def _config(self) -> Dict[str, Any]:
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
        backend_config: Dict[
            str, Any
        ] = self._backend.configuration().to_dict()
        keys: KeysView[str] = backend_config.keys()
        for k in config.keys():
            if k in keys:
                config[k] = backend_config[k]
        config["memory"] = False  # Bug(github): qiskit-terra #5415
        return config

    ############################# NUMPY INTERFACE #############################
    def random_raw(self) -> uint64:
        """Generate the next "raw" value, which is 64 bits"""
        bitstring: str = self.get_bitstring(64)
        random: int = int(bitstring, 2)
        return uint64(random)

    @property
    def next_64(self) -> Callable[[Any], uint64]:
        """
        Return a callable that accepts a single input and returns a numpy
        64-bit unsigned int. The input is usually a void pointer that is cast
        to a struct that contains the RNGs state. When wiring a bit generator
        in Python, it is simpler to use a closure than to wrap the state in an
        array, pass it's address as a ctypes void pointer, and then to get the
        pointer in the function.
        """

        def _next_64(void_p: Any) -> uint64:
            return self.random_raw()

        return _next_64

    @property
    def next_32(self) -> Callable[[Any], uint32]:
        """
        Return a callable that accepts a single input. This is identical to
        ``next_64`` except that it returns a numpy 32-bit unsigned int.
        """

        def _next_32(void_p: Any) -> uint32:
            bitstring: str = self.get_bitstring(32)
            random: int = int(bitstring, 2)
            return uint32(random)

        return _next_32

    @property
    def state_getter(self) -> Callable[[], Dict[str, Any]]:
        def f():
            return self.state

        return f

    @property
    def state_setter(self) -> Callable[[Dict[str, Any]], None]:
        def f(value: Dict[str, Any]) -> None:
            keys: KeysView[str] = value.keys()
            if "backend" in keys:
                self._backend = value["backend"]
            if "flush_bitcache" in keys:
                if value["flush_bitcache"]:
                    self._bitcache.flush()

        return f


###############################################################################
## QISKIT BIT GENERATOR WRAPPER FOR NUMPY
###############################################################################
def QiskitNumpyBitGenerator(
    provider: Optional[Provider] = None,
    backend: Optional[Backend] = None,
    bitgen: Optional[QiskitBitGenerator] = None,
) -> UserBitGenerator:
    if not bitgen:
        bitgen = QiskitBitGenerator(provider=provider, backend=backend)
    return UserBitGenerator(
        bitgen.next_64,
        64,
        next_32=bitgen.next_32,
        state_getter=bitgen.state_getter,
        state_setter=bitgen.state_setter,
    )
