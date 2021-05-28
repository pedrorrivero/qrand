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

from qsharp import QSharpCallable, azure, compile

from ...helpers import compute_bounded_factorization
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
        self.backend = backend
        self.circuit = circuit
        self.num_measurements = num_measurements  # type: ignore

    ############################### PUBLIC API ###############################
    @property
    def backend(self) -> QsharpBackend:
        return self._backend

    @backend.setter
    def backend(self, backend: QsharpBackend) -> None:
        self._backend: QsharpBackend = backend

    @property
    def circuit(self) -> QsharpCircuit:
        return self._circuit

    @circuit.setter
    def circuit(self, circuit: QsharpCircuit) -> None:
        if self.backend.max_qubits < circuit.num_qubits:
            raise RuntimeError(
                f"Failed to assign QsharpCircuit for QsharpJob. Number of \
                qubits in QsharpCircuit unsupported by this job's Backend: \
                {self.backend.max_qubits}<{circuit.num_qubits}."
            )
        self._circuit: QsharpCircuit = circuit

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

    def _generate_code(self) -> QSharpCallable:
        qsharp_code = """
        open Microsoft.Quantum.Intrinsic;
        open Microsoft.Quantum.Measurement;
        open Microsoft.Quantum.Arrays;

        operation Program():String[]{{

        use q = Qubit[{num_qubits}];
        mutable value = ConstantArray({num_qubits},"0");

        {gates}

        ResetAll(q);
        return value;
        }}
        """
        return compile(
            qsharp_code.format(
                num_qubits=self.circuit.num_qubits, gates=self.circuit.gates
            )
        )

    def execute(self) -> List[str]:
        self.program = self._generate_code()
        result: List[str] = []

        if self.backend.resource_id is None or self.backend.target_id is None:
            result = self.program.simulate()
        else:
            azure.connect(resourceId=self.backend.resource_id)
            azure.target(targetId=self.backend.target_id)
            result = azure.execute(
                self.program,
                shots=self.num_measurements,
                jobName="Generate random number",
            )
        return result

    @property
    def _experiments(self) -> int:
        return self.__experiments

    @_experiments.setter
    def _experiments(self, experiments: Optional[int]) -> None:
        self.__experiments: int = (
            experiments
            if experiments
            and type(experiments) is int
            and 0 < experiments < self.backend.max_experiments
            else self.backend.max_experiments
        )

    @property
    def _shots(self) -> int:
        return self.__shots

    @_shots.setter
    def _shots(self, shots: Optional[int]) -> None:
        self.__shots: int = (
            shots
            if shots
            and type(shots) is int
            and 0 < shots < self.backend.max_shots
            else self.backend.max_shots
        )
