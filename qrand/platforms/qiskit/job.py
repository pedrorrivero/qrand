##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: May 13, 2021
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

from typing import List, Optional
from warnings import warn

from qiskit import QuantumCircuit as QiskitQuantumCircuit
from qiskit import execute
from qiskit.providers import BackendV1 as Backend
from qiskit.providers import Job
from qiskit.result import Counts, Result

from ..circuit import QuantumCircuit
from ..job import QuantumJob
from .backend import QiskitBackend


###############################################################################
## QISKIT JOB
###############################################################################
class QiskitJob(QuantumJob):
    def __init__(
        self,
        circuit: QuantumCircuit,
        backend: Backend,
        shots: Optional[int] = None,
        experiments: Optional[int] = None,
    ) -> None:
        self.backend: QiskitBackend = backend  # type: ignore
        self.circuit: QuantumCircuit = circuit
        self.experiments: int = experiments  # type: ignore
        self.shots: int = shots  # type: ignore
        self._base_job: Optional[Job] = None

    ############################### PUBLIC API ###############################
    @property
    def backend(self) -> QiskitBackend:
        return self._backend

    @backend.setter
    def backend(self, backend: Backend) -> None:
        self._backend = QiskitBackend(backend)

    @property
    def circuit(self) -> QuantumCircuit:
        return self._circuit

    @circuit.setter
    def circuit(self, circuit: QuantumCircuit) -> None:
        if self.backend.max_num_qubits < circuit.num_qubits:
            raise RuntimeError(
                f"Failed to assign QiskitCircuit for QiskitJob. Number of \
                qubits in QiskitCircuit unsupported by the provided Backend: \
                {self.backend.max_num_qubits}<{circuit.num_qubits}."
            )
        self._circuit: QuantumCircuit = circuit

    @property
    def experiments(self) -> int:
        return self._experiments

    @experiments.setter
    def experiments(self, experiments: Optional[int]) -> None:
        experiments = (
            experiments
            if experiments and experiments > 1
            else self.backend.max_experiments
        )
        if self.backend.max_experiments < experiments:
            warn(
                f"Number of experiments unsupported by the provided Backend: \
                {self.backend.max_experiments}<{experiments}. \
                Using max_experiments instead.",
                UserWarning,
            )
            experiments = self.backend.max_experiments
        self._experiments: int = experiments

    @property
    def shots(self) -> int:
        return self._shots

    @shots.setter
    def shots(self, shots: Optional[int]) -> None:
        shots = shots if shots and shots > 1 else self.backend.max_shots
        if self.backend.max_shots < shots:
            warn(
                f"Number of shots unsupported by the provided Backend: \
                {self.backend.max_shots}<{shots}. Using max_shots instead.",
                UserWarning,
            )
            shots = self.backend.max_shots
        self._shots: int = shots

    @property
    def repetitions(self) -> int:
        return self.shots * self.experiments

    def execute(self) -> List[str]:
        circuits: List[QiskitQuantumCircuit] = [
            self.circuit
        ] * self.experiments
        self._base_job = execute(
            circuits,
            self.backend,
            shots=self.shots,
            memory=self._requires_memory,
        )
        result: Result = self._base_job.result()
        return self._parse_result(result)

    ############################### PRIVATE API ###############################
    @property
    def _requires_memory(self) -> bool:
        return True if self.shots > 1 else False

    @staticmethod
    def _reverse_string(string: str) -> str:
        return string[::-1]

    def _parse_result(self, result) -> List[str]:
        measurements: List[str] = []
        if self._requires_memory:
            for e in range(self.experiments):
                measurements += result.get_memory(e)
        else:
            cts = result.get_counts()
            counts: List[Counts] = [cts] if type(cts) != list else cts
            for c in counts:
                measurements += [k for k, v in c.items() if v == 1]
        num_qubits: int = self.circuit.num_qubits
        streams: List[str] = [""] * num_qubits
        for m in measurements:
            m = self._reverse_string(m)
            for q in range(num_qubits):
                streams[q] += m[q]
        return streams
