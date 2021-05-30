##    _____  _____
##   |  __ \|  __ \    AUTHOR: Avhijit Nair, Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: May 30, 2021
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

from qsharp import azure

from ...helpers import validate_type
from ..job import QuantumJob
from .backend import QsharpBackend
from .circuit import QsharpCircuit


###############################################################################
## QSHARP JOB
###############################################################################
class QsharpJob(QuantumJob):
    def __init__(
        self,
        circuit: QsharpCircuit,
        backend: QsharpBackend,
        num_measurements: Optional[int] = None,
    ) -> None:
        self.backend: QsharpBackend = backend
        self.circuit: QsharpCircuit = circuit
        self.num_measurements: int = num_measurements  # type: ignore

    ############################### PUBLIC API ###############################
    @property
    def backend(self) -> QsharpBackend:
        return self._backend

    @backend.setter
    def backend(self, backend: QsharpBackend) -> None:
        validate_type(backend, QsharpBackend)
        self._backend: QsharpBackend = backend

    @property
    def circuit(self) -> QsharpCircuit:
        return self._circuit

    @circuit.setter
    def circuit(self, circuit: QsharpCircuit) -> None:
        validate_type(circuit, QsharpCircuit)
        if self.backend.max_qubits < circuit.num_qubits:
            raise RuntimeError(
                f"Failed to assign QsharpCircuit for QsharpJob. Number of \
                qubits in QsharpCircuit unsupported by this job's Backend: \
                {self.backend.max_qubits}<{circuit.num_qubits}."
            )
        self._circuit: QsharpCircuit = circuit

    @property
    def num_measurements(self) -> int:  # type: ignore
        return self._num_measurements

    @num_measurements.setter
    def num_measurements(self, num_measurements: Optional[int]) -> None:
        num_measurements = (
            num_measurements
            if isinstance(num_measurements, int) and 0 < num_measurements
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
        self._num_measurements = num_measurements

    def execute(self) -> List[str]:
        self.program = self.circuit.generate_code(self.num_measurements)

        if self.backend.resource_id is None or self.backend.target_id is None:
            return self.program.simulate()
        else:
            azure.connect(resourceId=self.backend.resource_id)
            azure.target(targetId=self.backend.target_id)
            return azure.execute(
                self.program,
                shots=1,
                jobName="Generate random number",
            )
