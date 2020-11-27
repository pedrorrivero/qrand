##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: November 27, 2020
##   | |    | | \ \    ---------------------------------
##   |_|    |_|  \_\   https://github.com/pedrorrivero
##

## Copyright 2020 Pedro Rivero
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
## http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.

import struct
from typing import Any, Callable, Final, List, Optional, Tuple, Union

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
    _BACKEND_CONFIG_MASK: Final[dict] = {
        "backend_name": "",
        "credits_required": False,
        "local": True,
        "n_qubits": None,
        "simulator": True,
    }

    def __init__(
        self,
        provider: Optional[Provider] = None,
        backend: Optional[Backend] = None,
        backend_filter: Optional[BackendFilter] = None,
        max_bits_per_request: int = 0,
        ISRAW32: bool = False,
    ) -> None:
        if backend:
            provider = None
        elif provider:
            backend = self.get_best_backend(
                provider=provider,
                backend_filter=backend_filter,
            )
        else:
            backend = BasicAer.get_backend("qasm_simulator")
        self._provider: Optional[Provider] = provider
        self._backend: Backend = backend
        self._backend_filter: Optional[BackendFilter] = backend_filter
        self._set_mbpr(max_bits_per_request)
        self._ISRAW32: Final[bool] = ISRAW32
        self._bitcache: BitCache = BitCache()
        super().__init__(
            bits=self.bits,
            next_raw=self._next_raw,
            next_32=self._next_32,
            next_64=self._next_64,
            next_double=self._next_double,
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
        backend_filter: Optional[BackendFilter] = None,
    ) -> Backend:
        if not backend_filter:
            backend_filter = cls.default_backend_filter
        backends: List[Backend] = provider.backends(filters=backend_filter)
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

    def random_bitstring(self, n_bits: int = 0) -> str:
        if n_bits < 1:
            n_bits = self.bits
        while self._bitcache.size < n_bits:
            self._fetch_random_bits()
        return self._bitcache.pop(n_bits)

    def random_double(self, n: float = 1) -> float:
        """
        Returns a random double from a uniform distribution in the range
        [0,n). Defaults to [0,1).
        COPYRIGHT NOTICE:
        -----------------
        Source: https://github.com/ozanerhansha/qRNG
        License: GNU GENERAL PUBLIC LICENSE VERSION 3
        State changes:
            - Add static type hints
            - Limit range to [0,n) instead of [min,max) and add default
            - Replace call to original get_random_int64
        """
        unpacked = 0x3FF0000000000000 | self.random_uint(64) >> 12
        packed = struct.pack("Q", unpacked)
        value: float = struct.unpack("d", packed)[0] - 1.0
        return value * n

    def random_uint(self, n_bits: int = 0) -> int:
        if n_bits < 1:
            n_bits = self.bits
        return int(self.random_bitstring(n_bits), 2)

    def load_cache(self, bitstring: str, flush: bool = False) -> bool:
        if flush:
            return self._bitcache.flush() and self._bitcache.push(bitstring)
        return self._bitcache.push(bitstring)

    def set_state(
        self,
        provider: Optional[Provider] = None,
        backend: Optional[Backend] = None,
        backend_filter: Optional[BackendFilter] = None,
        max_bits_per_request: Optional[int] = None,
    ) -> bool:
        change: bool = False
        if max_bits_per_request is not None:
            change = True
            self._set_mbpr(max_bits_per_request)
        if backend_filter:
            change = True
            self._backend_filter = backend_filter
        if backend:
            change = True
            self._provider = None
            self._backend = backend
        elif provider:
            change = True
            self._provider = provider
            self._backend = self.get_best_backend(
                provider=provider,
                backend_filter=self._backend_filter,
            )
        return change

    ############################# PRIVATE METHODS #############################
    def _fetch_random_bits(self) -> bool:
        if self._provider:
            self._backend = self.get_best_backend(
                provider=self._provider,
                backend_filter=self._backend_filter,
            )
        circuits: List[QuantumCircuit] = [self._circuit] * self._experiments
        job: Job = execute(
            circuits,
            self._backend,
            shots=self._shots,
            memory=self._memory,
        )
        result: Result = job.result()
        bitstring: str = self._parse_result(result)
        self._bitcache.push(bitstring)
        return True

    def _parse_backend_config(self, backend_config: dict) -> dict:
        keys = backend_config.keys()
        config: dict = {}
        for k, v in self._BACKEND_CONFIG_MASK.items():
            config[k] = backend_config[k] if k in keys else v
        return config

    def _parse_result(self, result: Result) -> str:
        measurements: List[str] = []
        if self._memory:
            for e in range(self._experiments):
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

    def _set_mbpr(self, max_bits_per_request: int) -> bool:
        self._max_bits_per_request = (
            max_bits_per_request if max_bits_per_request > 0 else 0
        )
        return True

    ############################ PUBLIC PROPERTIES ############################
    @property
    def bits(self) -> int:
        """
        The number of bits output by the random_raw callable. Must be either
        32 or 64.
        """
        return 32 if self._ISRAW32 else 64

    @property
    def state(self) -> dict:
        s: dict = {
            "bits": self.bits,
            "job_config": self._job_config,
            "backend_config": self._parse_backend_config(self._backend_config),
            "dynamic_backend": {
                "filter": "Custom" if self._backend_filter else "Default",
            },
            "bitcache": self._bitcache.state,
        }
        if not self._provider:
            s.pop("dynamic_backend")
        return s

    @state.setter
    def state(self, value: dict) -> None:
        self.set_state(**value)

    ########################### PRIVATE PROPERTIES ###########################
    @property
    def _backend_config(self) -> dict:
        return self._backend.configuration().to_dict()

    @property
    def _circuit(self) -> QuantumCircuit:
        n_qubits: int = self._n_qubits
        qr: QuantumRegister = QuantumRegister(n_qubits)
        cr: ClassicalRegister = ClassicalRegister(n_qubits)
        circuit: QuantumCircuit = QuantumCircuit(qr, cr)
        circuit.h(qr)
        circuit.measure(qr, cr)
        return circuit

    @property
    def _experiments(self) -> int:
        n_qubits, shots, experiments = self._job_partition
        return experiments

    @property
    def _job_config(self) -> dict:
        return {
            "max_bits_per_request": self._max_bits_per_request or None,
            "bits_per_request": self._n_qubits
            * self._shots
            * self._experiments,
            "n_qubits": self._n_qubits,
            "shots": self._shots,
            "experiments": self._experiments,
        }

    @property
    def _job_partition(self) -> Tuple[int, int, int]:
        backend_config: dict = self._backend_config
        experiments: int = (
            backend_config["max_experiments"]
            if backend_config.__contains__("max_experiments")
            and backend_config["max_experiments"]
            else 1
        )
        shots: int = (
            backend_config["max_shots"]
            if backend_config.__contains__("max_shots")
            and backend_config["max_shots"]
            and backend_config.__contains__("memory")
            and backend_config["memory"]
            else 1
        )
        n_qubits: int = (
            backend_config["n_qubits"]
            if backend_config.__contains__("n_qubits")
            and backend_config["n_qubits"]
            else 1
        )
        max_bits_per_request: int = self._max_bits_per_request
        if max_bits_per_request > n_qubits:
            experiments = min(
                experiments,
                max_bits_per_request // (shots * n_qubits) + 1,
            )
            shots = min(
                shots,
                max_bits_per_request // (experiments * n_qubits),
            )
        elif max_bits_per_request > 0:
            experiments = 1
            shots = 1
            n_qubits = max_bits_per_request
        return n_qubits, shots, experiments

    @property
    def _memory(self) -> bool:
        return True if self._shots > 1 else False

    @property
    def _n_qubits(self) -> int:
        n_qubits, shots, experiments = self._job_partition
        return n_qubits

    @property
    def _shots(self) -> int:
        n_qubits, shots, experiments = self._job_partition
        return shots

    ############################# NUMPY INTERFACE #############################
    @property
    def _next_raw(self) -> Callable[[Any], Union[uint32, uint64]]:
        """
        A callable that returns either 64 or 32 random bits. It must accept
        a single input which is a void pointer to a memory address.
        """
        return self._next_32 if self._ISRAW32 else self._next_64

    @property
    def _next_32(self) -> Callable[[Any], uint32]:
        """
        A callable with the same signature as as next_raw that always returns
        a random numpy 32-bit unsigned int.
        """

        def next_32(void_p: Any) -> uint32:
            return uint32(self.random_uint(32))

        return next_32

    @property
    def _next_64(self) -> Callable[[Any], uint64]:
        """
        A callable with the same signature as as next_raw that always returns
        a random numpy 64-bit unsigned int.
        """

        def next_64(void_p: Any) -> uint64:
            return uint64(self.random_uint(64))

        return next_64

    @property
    def _next_double(self) -> Callable[[Any], float64]:
        """
        A callable with the same signature as as next_raw that always return
        a random double in [0,1).
        """

        def next_double(void_p: Any) -> float64:
            return float64(self.random_double(1))

        return next_double
