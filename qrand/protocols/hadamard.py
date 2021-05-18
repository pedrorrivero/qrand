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

from typing import List, Literal, Optional

from ..platforms.backend import QuantumBackend
from ..platforms.circuit import QuantumCircuit
from ..platforms.factory import QuantumFactory
from ..platforms.job import QuantumJob
from .protocol import BareQuantumProtocol
from .result import PlainResult, ProtocolResult


###############################################################################
## HADAMARD PROTOCOL
###############################################################################
class HadamardProtocol(BareQuantumProtocol):
    ############################### PUBLIC API ###############################
    def run(
        self, factory: QuantumFactory, max_bits: Optional[int] = None
    ) -> ProtocolResult:
        backend: QuantumBackend = factory.retrieve_backend(max_bits)
        num_qubits, num_measurements = backend.job_partition
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
    def _assemble_quantum_circuit(
        self, circuit: QuantumCircuit
    ) -> QuantumCircuit:
        for q in range(circuit.num_qubits):
            circuit.h(q)
            circuit.measure(q)
        return circuit

    def _parse_output(self, output: List[str]) -> ProtocolResult:
        bitstring: str = ""
        for measurement in output:
            bitstring += measurement
        return PlainResult(bitstring)
