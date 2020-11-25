##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: November 24, 2020
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
from qiskit.providers.ibmq import IBMQError, least_busy
from qiskit.providers.models import BackendConfiguration
from qiskit.result import Counts, Result
from randomgen import UserBitGenerator

###############################################################################
## CUSTOM TYPES
###############################################################################
BackendFilter = Callable[[Backend], bool]


###############################################################################
## BIT CACHE
###############################################################################
class BitCache:
    def __init__(self) -> None:
        self._cache: str = ""
        self.size: int = 0

    ########################## STATIC/CLASS METHODS ##########################
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
class QiskitBitGenerator(UserBitGenerator):
    _DEFAULT_CONFIG: Final[dict] = {
        "backend_name": "",
        "credits_required": False,
        "local": True,
        "max_experiments": None,
        "max_shots": None,
        "n_qubits": None,
        "simulator": True,
    }

    def __init__(
        self,
        provider: Optional[Provider] = None,
        backend: Optional[Backend] = None,
        backend_filter: Optional[BackendFilter] = None,
        israw32: bool = False,
    ) -> None:
        self.set_state(
            provider=provider,
            backend=backend,
            backend_filter=backend_filter,
        )
        self._bitcache: BitCache = BitCache()
        self._israw32: bool = israw32
        super().__init__(
            next_raw=self._next_raw,
            bits=self.bits,
            next_32=self._next_32,
            next_64=self._next_64,
            next_double=self._next_double,
            state_getter=self._state_getter,
            state_setter=self._state_setter,
        )

    ########################## STATIC/CLASS METHODS ##########################
    @staticmethod
    def default_backend_filter(b: Backend) -> bool:
        config: BackendConfiguration = b.configuration()
        return config.memory and not config.simulator

    @classmethod
    def get_best_backend(
        cls,
        provider: Provider,
        filter: Optional[BackendFilter] = None,
    ) -> Backend:
        if not filter:
            filter = cls.default_backend_filter
        backends: List[Backend] = provider.backends(filters=filter)
        if not backends:
            raise IBMQError(
                "No backends matching the filtering critera on the \
                requested provider."
            )
        return least_busy(backends)

    ############################# PUBLIC METHODS #############################
    def dump_cache(self, flush: bool = False) -> str:
        bitstring: str = self._bitcache.dump()
        if flush:
            self._bitcache.flush()
        return bitstring

    def flush_cache(self) -> bool:
        return self._bitcache.flush()

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

    def set_state(
        self,
        provider: Optional[Provider] = None,
        backend: Optional[Backend] = None,
        backend_filter: Optional[BackendFilter] = None,
    ) -> bool:
        if backend:
            provider = None
        else:
            backend = BasicAer.get_backend("qasm_simulator")
        self._provider: Optional[Provider] = provider
        self._backend: Backend = backend
        self._backend_filter: Optional[BackendFilter] = backend_filter
        return True

    ############################# PRIVATE METHODS #############################
    def _fetch_random_bits(self) -> bool:
        if self._provider:
            self._backend = self.get_best_backend(
                provider=self._provider, filter=self._backend_filter
            )
        circuits: List[QuantumCircuit] = [self._circuit] * self._config[
            "max_experiments"
        ]
        job: Job = execute(
            circuits,
            self._backend,
            shots=self._config["max_shots"],
            memory=self._memory,
        )
        result: Result = job.result()
        bitstring: str = self._parse_result(result)
        self._bitcache.push(bitstring)
        return True

    def _parse_result(self, result: Result) -> str:
        measurements: List[str] = []
        if self._memory:
            for e in range(self._config["max_experiments"]):
                measurements += result.get_memory(e)
        else:
            cts = result.get_counts()
            counts: List[Counts] = [cts] if type(cts) != list else cts
            for c in counts:
                measurements += [k for k, v in c.items() if v == 1]
        bitstring: str = ""
        for m in measurements:
            bitstring += m
        return bitstring

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
        s: dict = {
            "bits": self.bits,
            "dynamic_backend": {
                "filter": "Custom" if self._backend_filter else "Default",
            },
            "config": self._config,
            "bitcache": self._bitcache.state,
        }
        if not self._provider:
            s.pop("dynamic_backend")
        return s

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
        if not config["max_experiments"]:
            config["max_experiments"] = 1
        if not self._backend.configuration().memory:
            config["max_shots"] = 1
        return config

    @property
    def _memory(self):
        return True if self._config["max_shots"] > 1 else False

    ############################# NUMPY INTERFACE #############################
    @property
    def bits(self) -> int:
        """
        The number of bits output by the next_raw callable. Must be either
        32 or 64.
        """
        return 32 if self._israw32 else 64

    @property
    def _next_raw(self) -> Callable[[Any], Union[uint32, uint64]]:
        """
        A callable that returns either 64 or 32 random bits. It must accept
        a single input which is a void pointer to a memory address.
        """
        return self._next_32 if self._israw32 else self._next_64

    @property
    def _next_32(self) -> Callable[[Any], uint32]:
        """
        A callable with the same signature as as next_raw that always returns
        a random numpy 32-bit unsigned int.
        """

        def next_32(void_p: Any) -> uint32:
            return uint32(self.get_random_int(32))

        return next_32

    @property
    def _next_64(self) -> Callable[[Any], uint64]:
        """
        A callable with the same signature as as next_raw that always returns
        a random numpy 64-bit unsigned int.
        """

        def next_64(void_p: Any) -> uint64:
            return uint64(self.get_random_int(64))

        return next_64

    @property
    def _next_double(self) -> Callable[[Any], float64]:
        """
        A callable with the same signature as as next_raw that always return
        a random double in [0,1).
        """

        def next_double(void_p: Any) -> float64:
            return float64(self.get_random_double())

        return next_double

    @property
    def _state_getter(self) -> Callable[[], dict]:
        """A callable that returns the state of the bit generator."""

        def f():
            return self.state

        return f

    @property
    def _state_setter(self) -> Callable[[dict], None]:
        """
        A callable that sets the state of the bit generator. Must take a
        single input.
        """

        def f(value: dict) -> None:
            self.set_state(**value)

        return f
