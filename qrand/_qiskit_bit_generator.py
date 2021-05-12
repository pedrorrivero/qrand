##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: May 12, 2021
##   | |    | | \ \    ---------------------------------
##   |_|    |_|  \_\   https://github.com/pedrorrivero
##

## Copyright 2021 Pedro Rivero
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
from typing import Any, Callable, Final, List, Optional, Tuple
from warnings import warn

from qiskit import BasicAer, QuantumCircuit, execute
from qiskit.providers import Backend, Job, Provider
from qiskit.providers.ibmq import IBMQError, least_busy
from qiskit.providers.models import BackendConfiguration
from qiskit.result import Counts, Result

from .bit_cache import BitCache
from .quantum_bit_generator import QuantumBitGenerator

###############################################################################
## DEPRECATION WARNING -> warn(WARNING_MESSAGE, FutureWarning)
###############################################################################
WARNING_MESSAGE = "QiskitBitGenerator will be deprecated in version 1.0.0."
WARNING_MESSAGE += " Use QuantumBitGenerator and QiskitPlatform instead."


###############################################################################
## CUSTOM TYPES
###############################################################################
BackendFilter = Callable[[Backend], bool]


###############################################################################
## QISKIT BIT GENERATOR
###############################################################################
class QiskitBitGenerator(QuantumBitGenerator):
    """
    A quantum random bit-generator based on Qiskit, which can interface with
    NumPy's random module (e.g. to instantiate Generator objects). It
    implements an efficient strategy to retrieve random bits from IBMQ's quantum
    backends.

    PARAMETERS
    ----------
    provider: Optional[Provider] = None
        A Qiskit Provider object to access quantum backends.
        If `None` it defaults to BasicAer.
    backend: Optional[Backend] = None
        A Qiskit Backend object to produce random bits.
        If not `None`, `provider` will be ignored.
    backend_filter: Optional[BackendFilter] = None
        A Callable that takes in a Qiskit Backend object and returns `True`
        if it meets certain requirements, `False` otherwise. This is used
        to filter the list of available backends from which to dynamically
        choose on each request to the `provider` (if no `backend` is
        explicitly input). If `None` it defaults to
        `QiskitBitGenerator.default_backend_filter`.
    max_bits_per_request: int = 0
        A limit to the number of bits to be retrieved on each request to any
        Qiskit Backend. If less than one, no bound will be applied and the
        maximum allowed number of bits will be retrieved.
    ISRAW32: Final[bool] = False
        Toggle 32-bit BitGenerator mode. If `False` the BitGenerator will
        be 64-bit. This determines the number of bits returned by NumPy's
        `random_raw()` method, and the default number of bits to output on
        `random_uint()` and `random_double()`. Once an object is instantiated,
        this cannot be overridden.

    NOTES
    -----
    On each request to a backend, it retrieves as many bits as possible and
    stores them in a cache. This way, the number of internet connections
    leading to overheads is greatly reduced and, while the cache is loaded,
    random bits can be retrieved "instantaneously". The user can limit the
    number of bits to retrieve on each request through the
    `max_bits_per_request` parameter.
    Additionally, it always chooses the least busy backend from the list of
    machines available to the given provider. This list can be filtered by the
    user through the `backend_filter` parameter, which defaults to history-
    enabled non-simulators. If a Qiskit Backend is explicitly passed in as
    parameter, no backend selection will be performed: effectively ignoring any
    filters, or Qiskit Provider object passed.
    If neither `provider` nor `backend` are passed as inputs, it will default
    to running Qiskit BasicAer's 'qasm_simulator' locally.
    """

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
        warn(WARNING_MESSAGE, FutureWarning)
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
        self._ISRAW32: Final[bool] = ISRAW32  # type: ignore
        self._bitcache: BitCache = BitCache()
        super(QuantumBitGenerator, self).__init__(
            bits=self.BITS,
            next_raw=self._next_raw,
            next_32=self._next_32,
            next_64=self._next_64,
            next_double=self._next_double,
        )

    ########################## STATIC/CLASS METHODS ##########################
    @staticmethod
    def default_backend_filter(b: Backend) -> bool:
        """
        Default backend filter Callable.

        PARAMETERS
        ----------
        b: Backend
            A Qiskit Backend object.

        RETURNS
        -------
        out: bool
            `True` if `b` is not a simulator and has memory enabled, `False`
            otherwise.
        """
        config: BackendConfiguration = b.configuration()
        return config.memory and not config.simulator

    @classmethod
    def get_best_backend(
        cls,
        provider: Provider,
        backend_filter: Optional[BackendFilter] = None,
    ) -> Backend:
        """
        Returns the least busy backend available to an input provider, and
        according to certain filter(s).

        PARAMETERS
        ----------
        provider: Provider
            A Qiskit Provider object to access quantum backends.
        backend_filter: Optional[BackendFilter] = None
            A Callable that takes in a Qiskit Backend object and returns `True`
            if it meets certain requirements, `False` otherwise.
            If `None` it defaults to `cls.default_backend_filter`.

        RETURNS
        -------
        out: Backend
            Least busy backend from the filtered list of available backends.
        """
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
    def flush_cache(self) -> bool:  # type: ignore
        """
        Erase the cache.

        RETURNS
        -------
        out: bool
            `True` if succeeds, `False` otherwise.
        """
        return self._bitcache.flush()

    def load_cache(  # type: ignore
        self, bitstring: str, flush: bool = False
    ) -> bool:
        """
        Load cache contents from bitstring.

        PARAMETERS
        ----------
        bitstring: str
            The bitstring to load to cache.
        flush: bool
            If `True` erase cache before loading.

        RETURNS
        -------
        out: bool
            `True` if succeeds, `False` otherwise.

        RAISES
        ------
        TypeError (push)
            If input bitstring is not str
        ValueError (push)
            If input bitstring is not a valid bitstring
        """
        if flush:
            return self._bitcache.flush() and self._bitcache.push(bitstring)
        return self._bitcache.push(bitstring)

    def random_bitstring(self, n_bits: int = 0) -> str:
        """
        Returns a random bitstring of a given lenght. If less than one it
        defaults to the raw number of bits for the instance QiskitBitGenerator
        (i.e. 32 or 64).

        PARAMETERS
        ----------
        n_bits: int
            Number of bits to retrieve.

        RETURNS
        -------
        out: str
            Bitstring of lenght `n_bits`.
        """
        if n_bits < 1:
            n_bits = self.BITS
        while self._bitcache.size < n_bits:
            self._fetch_random_bits()
        return self._bitcache.pop(n_bits)

    def random_uint(self, n_bits: int = 0) -> int:
        """
        Returns a random unsigned int of a given size in bits.

        PARAMETERS
        ----------
        n_bits: int
            Number of bits to retrieve. If less than one it defaults to the raw
            number of bits for the instance QiskitBitGenerator (i.e. 32 or 64).

        RETURNS
        -------
        out: int
            Unsigned int of `n_bits` bits.
        """
        if n_bits < 1:
            n_bits = self.BITS
        return int(self.random_bitstring(n_bits), 2)

    def set_state(
        self,
        provider: Optional[Provider] = None,
        backend: Optional[Backend] = None,
        backend_filter: Optional[BackendFilter] = None,
        max_bits_per_request: Optional[int] = None,
    ) -> bool:
        """
        Override constructor parameters.
        Any change must be explicitly passed as input (i.e. not `None`).

        PARAMETERS
        ----------
        provider: Optional[Provider] = None
            Same as constructor.
        backend: Optional[Backend] = None
            Same as constructor.
        backend_filter: Optional[BackendFilter] = None
            Same as constructor.
        max_bits_per_request: Optional[int] = None
            Same as constructor.

        RETURNS
        -------
        out: bool
            `True` if any changes were made, `False` otherwise.
        """
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
    def state(self) -> dict:
        """
        Parsed information about the current state of the QiskitBitGenerator.
        """
        s: dict = {
            "BITS": self.BITS,
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
        """
        An alternative form of `set_state()` parsed from dict equality.
        """
        self.set_state(**value)

    ########################### PRIVATE PROPERTIES ###########################
    @property
    def _backend_config(self) -> dict:
        return self._backend.configuration().to_dict()

    @property
    def _circuit(self) -> QuantumCircuit:
        n_qubits: int = self._n_qubits
        circuit: QuantumCircuit = QuantumCircuit(n_qubits)
        circuit.h(range(n_qubits))
        circuit.measure_all()
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
