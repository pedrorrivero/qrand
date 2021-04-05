##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: March 29, 2021
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
from qiskit.providers import Backend, Provider
from qiskit.providers.ibmq import IBMQError, least_busy
from qiskit.providers.models import BackendConfiguration

from .._quantum_protocols import ProtocolResult, QuantumProtocol
from . import QuantumPlatform
from ._quantum_circuits import QiskitCircuit, QuantumCircuit
from ._quantum_jobs import QiskitJob, QuantumJob

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
        max_bits_per_request: int = 0,
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

    ############################### PUBLIC API ###############################
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

    def create_circuit(
        self, num_qubits: Optional[int] = None
    ) -> QuantumCircuit:
        if not num_qubits:
            num_qubits = self._num_qubits
        return QiskitCircuit(num_qubits)

    def create_job(
        self, circuit: QuantumCircuit, max_repetitions: Optional[int] = None
    ) -> QuantumJob:
        num_qubits, shots, experiments = self._job_partition
        if num_qubits != circuit.num_qubits:
            raise RuntimeError(
                f"Failed to create QiskitJob. Invalid number of qubits in \
                argument QiskitCircuit: {circuit.num_qubits}!={num_qubits}."
            )
        if max_repetitions:
            if shots >= max_repetitions:
                shots = max_repetitions
                experiments = 1
            else:
                e = max_repetitions // shots
                experiments = min(e, experiments)
        return QiskitJob(circuit, self._backend, shots, experiments)

    def fetch_random_bits(self, protocol: QuantumProtocol) -> str:
        self.refresh()
        result: ProtocolResult = protocol.run(self)
        return result.bitstring

    def refresh(self) -> None:
        if self._provider:
            self._backend = self.get_best_backend(
                provider=self._provider,
                backend_filter=self._backend_filter,
            )

    ############################### PRIVATE API ###############################
    @property
    def _backend_config(self) -> dict:
        return self._backend.configuration().to_dict()

    @property
    def _experiments(self) -> int:
        num_qubits, shots, experiments = self._job_partition
        return experiments

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
        num_qubits: int = (
            backend_config["num_qubits"]
            if backend_config.__contains__("num_qubits")
            and backend_config["num_qubits"]
            else 1
        )
        max_bits_per_request: int = self._max_bits_per_request
        if max_bits_per_request > num_qubits:
            experiments = min(
                experiments,
                max_bits_per_request // (shots * num_qubits) + 1,
            )
            shots = min(
                shots,
                max_bits_per_request // (experiments * num_qubits),
            )
        elif max_bits_per_request > 0:
            experiments = 1
            shots = 1
            num_qubits = max_bits_per_request
        return num_qubits, shots, experiments

    @property
    def _num_qubits(self) -> int:
        num_qubits, shots, experiments = self._job_partition
        return num_qubits

    @property
    def _shots(self) -> int:
        num_qubits, shots, experiments = self._job_partition
        return shots

    def _set_mbpr(self, max_bits_per_request: int) -> None:
        self._max_bits_per_request = (
            max_bits_per_request if max_bits_per_request > 0 else 0
        )
