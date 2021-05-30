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

from typing import Optional

from ...protocols import ProtocolResult
from ..platform import QuantumPlatform, QuantumProtocol
from .backend import QsharpBackend
from .circuit import QsharpCircuit
from .job import QsharpJob


###############################################################################
## QSHARP PLATFORM
###############################################################################
class QsharpPlatform(QuantumPlatform):
    def __init__(
        self,
        resource_id: Optional[str] = None,
        target_id: Optional[str] = None,
    ) -> None:
        self.resource_id = resource_id
        self.target_id = target_id

    ############################### PUBLIC API ###############################
    def create_circuit(self, num_qubits: int) -> QsharpCircuit:
        return QsharpCircuit(num_qubits)

    def create_job(  # type: ignore
        self,
        circuit: QsharpCircuit,
        backend: QsharpBackend,
        num_measurements: Optional[int] = None,
    ) -> QsharpJob:
        return QsharpJob(circuit, backend, num_measurements)

    def fetch_random_bits(self, protocol: QuantumProtocol) -> str:
        result: ProtocolResult = protocol.run(self)
        return result.bitstring

    def retrieve_backend(self) -> QsharpBackend:
        return QsharpBackend(self.resource_id, self.target_id)
