##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: May 17, 2021
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
from qiskit.providers import Job
from qiskit.result import Counts, Result

from ...helpers import compute_bounded_factorization, reverse_endian
from ..job import QuantumJob
from .backend import QiskitBackend
from .circuit import QiskitCircuit


###############################################################################
## QISKIT JOB
###############################################################################
class QiskitJob(QuantumJob):
    def __init__(
        self,
        circuit: QiskitCircuit,
        backend: QiskitBackend,
        num_measurements: Optional[int] = None,
    ) -> None:
        self.backend: QiskitBackend = backend
        self.circuit: QiskitCircuit = circuit
        self.num_measurements: int = num_measurements  # type: ignore
        self._base_job: Optional[Job] = None

    ############################### PUBLIC API ###############################
    @property
    def backend(self) -> QiskitBackend:
        return self._backend

    @backend.setter
    def backend(self, backend: QiskitBackend) -> None:
        self._backend: QiskitBackend = backend

    @property
    def circuit(self) -> QiskitCircuit:
        return self._circuit

    @circuit.setter
    def circuit(self, circuit: QiskitCircuit) -> None:
        if self.backend.max_qubits < circuit.num_qubits:
            raise RuntimeError(
                f"Failed to assign QiskitCircuit for QiskitJob. Number of \
                qubits in QiskitCircuit unsupported by this job's Backend: \
                {self.backend.max_qubits}<{circuit.num_qubits}."
            )
        self._circuit: QiskitCircuit = circuit

    @property
    def num_measurements(self) -> int:
        return self._shots * self._experiments

    @num_measurements.setter
    def num_measurements(self, num_measurements: Optional[int]) -> None:
        num_measurements = (
            num_measurements
            if num_measurements
            and type(num_measurements) is int
            and 0 < num_measurements
            else self.backend.max_measurements
        )
        if self.backend.max_measurements < num_measurements:
            warn(
                f"Number of measurements unsupported by the job's Backend: \
                {self.backend.max_measurements}<{num_measurements}. \
                Using max_measurements instead.",
                UserWarning,
            )
            num_measurements = self.backend.max_measurements
        self._shots, self._experiments = compute_bounded_factorization(
            num_measurements,
            self.backend.max_shots,
            self.backend.max_experiments,
        )

    def execute(self) -> List[str]:
        circuits: List[QiskitQuantumCircuit] = [
            self.circuit
        ] * self._experiments
        self._base_job = execute(
            circuits,
            self.backend,
            shots=self._shots,
            memory=self._requires_memory,
        )
        result: Result = self._base_job.result()
        return self._parse_result(result)

    ############################### PRIVATE API ###############################
    @property
    def _experiments(self) -> int:
        return self.__experiments

    @_experiments.setter
    def _experiments(self, experiments: Optional[int]) -> None:
        self.__experiments: int = (
            experiments
            if type(experiments) is int
            and 0 < experiments < self.backend.max_experiments  # type: ignore
            else self.backend.max_experiments
        )

    @property
    def _requires_memory(self) -> bool:
        return True if self._shots > 1 else False

    @property
    def _shots(self) -> int:
        return self.__shots

    @_shots.setter
    def _shots(self, shots: Optional[int]) -> None:
        self.__shots: int = (
            shots
            if type(shots) is int
            and 0 < shots < self.backend.max_shots  # type: ignore
            else self.backend.max_shots
        )

    def _parse_result(self, result: Result) -> List[str]:
        measurements: List[str] = []
        if self._requires_memory:
            for e in range(self._experiments):
                measurements += result.get_memory(e)
        else:
            cts = result.get_counts()
            counts: List[Counts] = [cts] if type(cts) != list else cts
            for c in counts:
                measurements += [k for k, v in c.items() if v == 1]
        return reverse_endian(measurements)  # type: ignore
