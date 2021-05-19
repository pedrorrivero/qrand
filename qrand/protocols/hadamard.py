##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: May 19, 2021
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

from typing import List, Literal, Optional, Tuple

from ..helpers import compute_bounded_factorization
from ..platforms.backend import QuantumBackend
from ..platforms.circuit import QuantumCircuit
from ..platforms.factory import QuantumFactory
from ..platforms.job import QuantumJob
from .protocol import BareQuantumProtocol
from .result import BasicResult


###############################################################################
## HADAMARD PROTOCOL
###############################################################################
class HadamardProtocol(BareQuantumProtocol):
    ############################### PUBLIC API ###############################
    def run(
        self, factory: QuantumFactory, max_bits: Optional[int] = None
    ) -> BasicResult:
        backend: QuantumBackend = factory.retrieve_backend()
        num_qubits, num_measurements = self._job_partition(
            max_bits, backend.max_qubits, backend.max_measurements
        )
        circuit: QuantumCircuit = factory.create_circuit(num_qubits)
        circuit = self._assemble_quantum_circuit(circuit)
        job: QuantumJob = factory.create_job(
            circuit, backend, num_measurements
        )
        output: List[str] = job.execute()
        return self._parse_output(output)

    def verify(self) -> Literal[False]:
        return False

    ############################### PRIVATE API ###############################
    @staticmethod
    def _assemble_quantum_circuit(circuit: QuantumCircuit) -> QuantumCircuit:
        for q in range(circuit.num_qubits):
            circuit.h(q)
            circuit.measure(q)
        return circuit

    @staticmethod
    def _job_partition(
        bits: Optional[int], max_qubits: int, max_measurements: int
    ) -> Tuple[int, int]:
        return (
            compute_bounded_factorization(bits, max_qubits, max_measurements)
            if bits and type(bits) is int and bits > 0
            else (max_qubits, max_measurements)
        )

    @staticmethod
    def _parse_output(output: List[str]) -> BasicResult:
        bitstring: str = ""
        for measurement in output:
            bitstring += measurement
        return BasicResult(bitstring)
