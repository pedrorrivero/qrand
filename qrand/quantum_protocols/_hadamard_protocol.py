##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: March 28, 2021
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

from typing import List, Literal

from ..quantum_platforms import QuantumCircuit, QuantumJob, QuantumPlatform
from . import ProtocolResult, ProtocolStrategy, SimpleResult


###############################################################################
## HADAMARD PROTOCOL
###############################################################################
class HadamardProtocol(ProtocolStrategy):
    ############################### PUBLIC API ###############################
    def run(self, platform: QuantumPlatform) -> ProtocolResult:
        circuit: QuantumCircuit = self._build_quantum_circuit(platform)
        job: QuantumJob = platform.create_job(circuit)
        output: List[str] = job.execute()
        return self._parse_output(output)

    def verify(self) -> Literal[False]:
        return False

    ############################### PRIVATE API ###############################
    def _build_quantum_circuit(
        self, platform: QuantumPlatform
    ) -> QuantumCircuit:
        circuit: QuantumCircuit = platform.create_circuit()
        for q in range(circuit.num_qubits):
            circuit.h(q)
            circuit.measure(q)
        return circuit

    def _parse_output(self, output: List[str]) -> ProtocolResult:
        bitstring: str = ""
        for stream in output:
            bitstring += stream
        return SimpleResult(bitstring)
