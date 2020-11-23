##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: November 23, 2020
##   | |    | | \ \    ---------------------------------
##   |_|    |_|  \_\   https://github.com/pedrorrivero
##

import struct
from typing import Any, Callable, Final, List, Optional, Union

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
        b = {"0", "1"}
        s = set(bitstring)
        return s.issubset(b)

    ############################# PUBLIC METHODS #############################
    def dump(self) -> str:
        return self._cache

    def flush(self) -> bool:
        self._cache = ""
        self.size = 0
        return True

    def pop(self, n: int) -> str:
        bitstring: str = self._cache[:n]
        self._cache = self._cache[n:]
        self.size -= n if n < self.size else self.size
        return bitstring

    def push(self, bitstring: str) -> bool:
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
    _DEFAULT_CONFIG: Final[dict] = {
        "backend_name": "",
        "credits_required": False,
        "local": True,
        "max_experiments": None,
        "max_shots": None,
        "memory": False,
        "n_qubits": None,
        "simulator": True,
    }

    def __init__(
        self,
        provider: Optional[Provider] = None,
        backend: Optional[Backend] = None,
        israw32: bool = False,
    ) -> None:
        if provider and not backend:
            backend = self.get_best_backend(provider)
        if not backend:
            backend = BasicAer.get_backend("qasm_simulator")
        self._backend: Backend = backend
        self._provider: Provider = backend.provider
        self._bitcache: BitCache = BitCache()
        self._israw32: bool = israw32

    ############################# STATIC METHODS #############################
    @staticmethod
    def get_best_backend(provider: Provider) -> Optional[Backend]:
        def filters(b: Backend) -> bool:
            config: BackendConfiguration = b.configuration()
            return config.memory and not config.simulator

        backends: List[Backend] = provider.backends(filters=filters)
        return least_busy(backends) if backends else None

    ############################# PUBLIC METHODS #############################
    def dump_cache(self, flush: bool = False) -> str:
        bitstring: str = self._bitcache.dump()
        if flush:
            self._bitcache.flush()
        return bitstring

    def get_random_bitstring(self, n_bits: int) -> str:
        while self._bitcache.size < n_bits:
            self._fetch_random_bits()
        return self._bitcache.pop(n_bits)

    def get_random_double(self, min: float = 0, max: float = 1) -> float:
        """
        Returns a random double from a uniform distribution in the range
        [min, max). Defaults to [0, 1).
        COPYRIGHT NOTICE:
        -----------------
        Source: https://github.com/ozanerhansha/qRNG
        License: GNU GENERAL PUBLIC LICENSE VERSION 3
        State changes:
            - Add static type hints
            - Add default range
            - Replace call to original get_random_int64
        """
        unpacked = 0x3FF0000000000000 | self.get_random_int(64) >> 12
        packed = struct.pack("Q", unpacked)
        value: float = struct.unpack("d", packed)[0] - 1.0
        return (max - min) * value + min

    def get_random_int(self, n_bits: int) -> int:
        return int(self.get_random_bitstring(n_bits), 2)

    def load_cache(self, bitstring: str, flush: bool = False) -> bool:
        if flush:
            return self._bitcache.flush() and self._bitcache.push(bitstring)
        return self._bitcache.push(bitstring)

    ############################# PRIVATE METHODS #############################
    def _fetch_random_bits(self) -> bool:
        circuits: List[QuantumCircuit] = [self._circuit] * self._config[
            "max_experiments"
        ]
        job: Job = execute(
            circuits, self._backend, shots=self._config["max_shots"]
        )
        result: Result = job.result()
        measurements: List[str] = self._parse_result(result)
        for m in measurements:
            self._bitcache.push(m)
        return True

    def _parse_result(self, result: Result) -> List[str]:
        if self._config["memory"]:
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

    def _parse_backend_config(self) -> dict:
        backend_config: dict = self._backend.configuration().to_dict()
        keys = backend_config.keys()
        config: dict = {}
        for k, v in self._DEFAULT_CONFIG.items():
            config[k] = backend_config[k] if k in keys else v
        return config

    ############################ PUBLIC PROPERTIES ############################
    @property
    def state(self) -> dict:
        return {
            "bits": self.bits,
            "config": self._config,
            "bitcache": self._bitcache.state,
        }

    ########################### PRIVATE PROPERTIES ###########################
    @property
    def _circuit(self) -> QuantumCircuit:
        n_qubits: int = self._config["n_qubits"]
        qr: QuantumRegister = QuantumRegister(n_qubits)
        cr: ClassicalRegister = ClassicalRegister(n_qubits)
        circuit: QuantumCircuit = QuantumCircuit(qr, cr)
        circuit.h(qr)
        circuit.measure(qr, cr)
        return circuit

    @property
    def _config(self) -> dict:
        config: dict = self._parse_backend_config()
        config["memory"] = False  # Bug(github): qiskit-terra #5415
        if not config["max_experiments"]:
            config["max_experiments"] = 1
        if not config["memory"]:
            config["max_shots"] = 1
        return config

    ############################# NUMPY INTERFACE #############################
    @property
    def random_raw(self) -> Callable[[Any], Union[uint32, uint64]]:
        """
        A callable that returns either 64 or 32 random bits. It must accept
        a single input which is a void pointer to a memory address.
        """
        return self.next_32 if self._israw32 else self.next_64

    @property
    def bits(self) -> int:
        """
        The number of bits output by the next_raw callable. Must be either
        32 or 64.
        """
        return 32 if self._israw32 else 64

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
            return float64(self.get_random_double())

        return _next_double

    @property
    def state_getter(self) -> Callable[[], dict]:
        """A callable that returns the state of the bit generator."""

        def f():
            return self.state

        return f

    @property
    def state_setter(self) -> Callable[[dict], None]:
        """
        A callable that sets the state of the bit generator. Must take a
        single input.
        """

        def f(value: dict) -> None:
            keys = value.keys()
            if "backend" in keys:
                self._backend = value["backend"]
            if "israw32" in keys:
                self._israw32 = value["israw32"]
            if "flush_cache" in keys:
                if value["flush_cache"]:
                    self._bitcache.flush()

        return f


###############################################################################
## QISKIT BIT GENERATOR FOR NUMPY (FACTORY)
###############################################################################
def QiskitNumpyBitGenerator(
    provider: Optional[Provider] = None,
    backend: Optional[Backend] = None,
    israw32: bool = False,
    bitgen: Optional[QiskitBitGenerator] = None,
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
