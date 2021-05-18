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

from typing import Optional, Tuple

from ..platform import QuantumPlatform, QuantumProtocol
from .backend import CirqBackend
from .circuit import CirqCircuit
from .job import CirqJob


###############################################################################
## CIRQ PLATFORM
###############################################################################
class CirqPlatform(QuantumPlatform):
    def __init__(self) -> None:
        self.ERROR_MSG = f"{self.__class__.__name__}"  # TODO
        raise NotImplementedError(self.ERROR_MSG)

    ############################### PUBLIC API ###############################
    def create_circuit(self, num_qubits: int) -> CirqCircuit:
        raise NotImplementedError(self.ERROR_MSG)

    def create_job(  # type: ignore
        self,
        circuit: CirqCircuit,
        backend: CirqBackend,
        num_measurements: Optional[int] = None,
    ) -> CirqJob:
        raise NotImplementedError(self.ERROR_MSG)

    def fetch_random_bits(self, protocol: QuantumProtocol) -> str:
        raise NotImplementedError(self.ERROR_MSG)

    def retrieve_backend(
        self, max_bits_per_request: Optional[int] = None
    ) -> CirqBackend:
        raise NotImplementedError(self.ERROR_MSG)
