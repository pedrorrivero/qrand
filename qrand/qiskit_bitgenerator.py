##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: November 21, 2020
##   | |    | | \ \    ---------------------------------
##   |_|    |_|  \_\   https://github.com/pedrorrivero
##

import struct
from typing import Any, Callable, Dict, KeysView, List, Optional, Set, Union

from numpy import float64, uint32, uint64
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
    def state(self) -> Dict[str, Any]:
        return {"size": self.size}


###############################################################################
## QISKIT BIT GENERATOR
###############################################################################
class QiskitBitGenerator:
    def __init__(
        self,
        provider: Optional[Provider] = None,
        backend: Optional[Backend] = None,
        israw32: bool = False,
    ) -> None:
        if provider and not backend:
            backend = QiskitBitGenerator.get_best_backend(provider)
        if not backend:
            backend = BasicAer.get_backend("qasm_simulator")
        self._backend: Backend = backend
        self._provider: Provider = backend.provider
        self._bitcache: BitCache = BitCache()
        self.israw32: bool = israw32

    ############################# STATIC METHODS #############################
    @staticmethod
    def get_best_backend(provider: Provider) -> Optional[Backend]:
        def filters(b: Backend) -> bool:
            config: BackendConfiguration = b.configuration()
            return config.memory and not config.simulator

        backends: List[Backend] = provider.backends(filters=filters)
        return least_busy(backends) if backends else None

    ############################# PUBLIC METHODS #############################
    def get_random_bitstring(self, n_bits: int) -> str:
        while self._bitcache.size < n_bits:
            self._fetch_random_bits()
        return self._bitcache.get(n_bits)

    def get_random_int(self, n_bits: int) -> int:
        return int(self.get_random_bitstring(n_bits), 2)

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
        config: Dict[str, Any] = {
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
    @property
    def random_raw(self) -> Callable[[Any], Union[uint32, uint64]]:
        """
        A callable that returns either 64 or 32 random bits. It must accept
        a single input which is a void pointer to a memory address.
        """

        if self.israw32:
            return self.next_32
        else:
            return self.next_64

    @property
    def bits(self) -> int:
        """
        The number of bits output by the next_raw callable. Must be either
        32 or 64.
        """

        return 32 if self.israw32 else 64

    @property
    def next_32(self) -> Callable[[Any], uint32]:
        """
        A callable with the same signature as as next_raw that always returns
        a random numpy 32-bit unsigned int.
        """

        def _next_32(void_p: Any) -> uint32:
            return uint32(self.get_random_int(32))

        return _next_32

    @property
    def next_64(self) -> Callable[[Any], uint64]:
        """
        A callable with the same signature as as next_raw that always returns
        a random numpy 64-bit unsigned int.
        """

        def _next_64(void_p: Any) -> uint64:
            return uint64(self.get_random_int(64))

        return _next_64

    @property
    def next_double(self) -> Callable[[Any], float64]:
        """
        A callable with the same signature as as next_raw that always return
        a random double in [0,1).
        """

        def _next_double(void_p: Any) -> float64:
            unpacked = 0x3FF0000000000000 | self.get_random_int(64) >> 12
            packed = struct.pack("Q", unpacked)
            random = struct.unpack("d", packed)[0] - 1.0
            return float64(random)

        return _next_double

    @property
    def state_getter(self) -> Callable[[], Dict[str, Any]]:
        """A callable that returns the state of the bit generator."""

        def f():
            return self.state

        return f

    @property
    def state_setter(self) -> Callable[[Dict[str, Any]], None]:
        """
        A callable that sets the state of the bit generator. Must take a
        single input.
        """

        def f(value: Dict[str, Any]) -> None:
            keys: KeysView[str] = value.keys()
            if "backend" in keys:
                self._backend = value["backend"]
            if "flush_bitcache" in keys:
                if value["flush_bitcache"]:
                    self._bitcache.flush()

        return f


###############################################################################
## QISKIT BIT GENERATOR FOR NUMPY (FACTORY)
###############################################################################
def QiskitNumpyBitGenerator(
    provider: Optional[Provider] = None,
    backend: Optional[Backend] = None,
    bitgen: Optional[QiskitBitGenerator] = None,
    israw32: bool = False,
) -> UserBitGenerator:
    if not bitgen:
        bitgen = QiskitBitGenerator(
            provider=provider, backend=backend, israw32=israw32
        )
    return UserBitGenerator(
        bitgen.random_raw,
        bits=bitgen.bits,
        next_32=bitgen.next_32,
        next_64=bitgen.next_64,
        next_double=bitgen.next_double,
        state_getter=bitgen.state_getter,
        state_setter=bitgen.state_setter,
    )
