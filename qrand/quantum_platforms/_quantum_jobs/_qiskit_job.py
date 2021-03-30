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

from typing import List, Optional

from qiskit import QuantumCircuit as QiskitQuantumCircuit
from qiskit import execute
from qiskit.providers import Backend, Job
from qiskit.result import Counts, Result

from .._quantum_circuits import QuantumCircuit
from . import QuantumJob


###############################################################################
## QISKIT JOB
###############################################################################
class QiskitJob(QuantumJob):
    def __init__(
        self,
        circuit: QuantumCircuit,
        shots: int,
        experiments: int,
        backend: Backend,
    ) -> None:
        self._backend: Backend = backend
        self._base_job: Optional[Job] = None
        self._circuit: QuantumCircuit = circuit
        self._experiments: int = experiments
        self._shots: int = shots

    def execute(self) -> List[str]:
        circuits: List[QiskitQuantumCircuit] = [
            self._circuit.extract_base_circuit()
        ] * self._experiments
        self._base_job = execute(
            circuits,
            self._backend,
            shots=self._shots,
            memory=self._memory,
        )
        result: Result = self._base_job.result()
        return self._parse_result(result)

    def extract_base_job(self) -> Job:
        return self._base_job

    def _parse_result(self, result) -> List[str]:
        measurements: List[str] = []
        if self._memory:
            for e in range(self._experiments):
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

    @staticmethod
    def _reverse_string(string: str) -> str:
        return string[::-1]

    @property
    def circuit(self) -> QuantumCircuit:
        return self._circuit

    @property
    def _memory(self) -> bool:
        return True if self._shots > 1 else False
