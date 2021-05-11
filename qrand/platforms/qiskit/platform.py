##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: May 11, 2021
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

from typing import Callable, List, Optional, Tuple

from qiskit import BasicAer
from qiskit.providers import BackendV1 as Backend
from qiskit.providers import Provider
from qiskit.providers.ibmq import IBMQError, least_busy
from qiskit.providers.models import BackendConfiguration

from ..circuit import QuantumCircuit
from ..job import QuantumJob
from ..platform import ProtocolResult, QuantumPlatform, QuantumProtocol
from .backend import QiskitBackend
from .circuit import QiskitCircuit
from .job import QiskitJob

###############################################################################
## CUSTOM TYPES
###############################################################################
BackendFilter = Callable[[Backend], bool]


###############################################################################
## QISKIT PLATFORM
###############################################################################
class QiskitPlatform(QuantumPlatform):
    def __init__(
        self,
        provider: Optional[Provider] = None,
        backend: Optional[Backend] = None,
        backend_filter: Optional[BackendFilter] = None,
        max_bits_per_request: Optional[int] = None,
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
        self.provider: Optional[Provider] = provider
        self.backend: QiskitBackend = backend  # type: ignore
        self.backend_filter: BackendFilter = backend_filter  # type: ignore
        self.max_bits_per_request: int = max_bits_per_request  # type: ignore

    ############################### PUBLIC API ###############################
    @property
    def backend(self) -> QiskitBackend:
        return self._backend

    @backend.setter
    def backend(self, backend: Backend) -> None:
        self._backend: QiskitBackend = QiskitBackend(backend)

    @property
    def backend_filter(self) -> BackendFilter:
        return self._backend_filter

    @backend_filter.setter
    def backend_filter(self, backend_filter: Optional[BackendFilter]) -> None:
        self._backend_filter = backend_filter or self.default_backend_filter

    @property
    def job_partition(self) -> Tuple[int, int]:
        num_qubits, shots, experiments = self._qiskit_job_partition
        repetitions: int = shots * experiments
        return num_qubits, repetitions

    @property
    def max_bits_per_request_allowed(self) -> int:
        return (
            self.backend.max_num_qubits
            * self.backend.max_shots
            * self.backend.max_experiments
        )

    @property
    def provider(self) -> Optional[Provider]:
        return self._provider

    @provider.setter
    def provider(self, provider: Optional[Provider]) -> None:
        self._provider = provider

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
            raise IBMQError(  # TODO
                "No backends matching the filtering critera on the \
                requested provider."
            )
        return least_busy(backends)

    def create_circuit(self, num_qubits: int) -> QuantumCircuit:
        return QiskitCircuit(num_qubits)

    def create_job(
        self, circuit: QuantumCircuit, repetitions: int
    ) -> QuantumJob:
        shots, experiments = self._compute_bounded_factorization(
            repetitions, self.backend.max_shots, self.backend.max_experiments
        )
        return QiskitJob(circuit, self.backend, shots, experiments)

    def fetch_random_bits(self, protocol: QuantumProtocol) -> str:
        self.refresh()
        result: ProtocolResult = protocol.run(self)
        return result.bitstring

    def refresh(self) -> None:
        if self.provider:
            self.backend = self.get_best_backend(
                provider=self.provider,
                backend_filter=self.backend_filter,
            )

    ############################### PRIVATE API ###############################
    @staticmethod
    def _compute_bounded_factorization(
        n: int, bound_A: int, bound_B: int
    ) -> Tuple[int, int]:
        if not bound_A * bound_B > n:
            return bound_A, bound_B
        swapped: bool = bound_A > bound_B
        bound_A, bound_B = sorted([bound_A, bound_B])
        final_b: int = bound_B
        final_a: int = n // final_b
        final_delta: int = n - final_a * final_b
        a: int = final_a + 1
        b: int = n // a
        delta: int = n - a * b
        while a <= bound_A and a <= b and final_delta != 0:
            if delta < final_delta:
                final_a, final_b, final_delta = a, b, delta
            a += 1
            b = n // a
            delta = n - a * b
        return (final_b, final_a) if swapped else (final_a, final_b)

    @property
    def _qiskit_job_partition(self) -> Tuple[int, int, int]:
        experiments: int = self.backend.max_experiments
        shots: int = self.backend.max_shots
        num_qubits: int = self.backend.max_num_qubits
        max_bits_per_request: int = self.max_bits_per_request
        if max_bits_per_request > num_qubits:
            repetitions: int = max_bits_per_request // num_qubits
            shots, experiments = self._compute_bounded_factorization(
                repetitions,
                self.backend.max_shots,
                self.backend.max_experiments,
            )
        elif max_bits_per_request > 0:
            experiments = 1
            shots = 1
            num_qubits = max_bits_per_request
        return num_qubits, shots, experiments
