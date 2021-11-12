# _____  _____
# |  __ \|  __ \    AUTHOR: Pedro Rivero
# | |__) | |__) |   ---------------------------------
# |  ___/|  _  /    DATE: May 20, 2021
# | |    | | \ \    ---------------------------------
# |_|    |_|  \_\   https://github.com/pedrorrivero
##

# Copyright 2021 Pedro Rivero
##
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
##
# http://www.apache.org/licenses/LICENSE-2.0
##
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Optional

from ...helpers import validate_type
from ...protocols import ProtocolResult, QuantumProtocol

from ..platform import QuantumPlatform
from .backend import CirqBackend
from .circuit import CirqCircuit
from .job import CirqJob

from cirq_google import Engine
from cirq.sim import simulator
###############################################################################
# CIRQ PLATFORM
###############################################################################


class CirqPlatform(QuantumPlatform):
    def __init__(
         self,
         engine: Optional[Engine] = None,
     ) -> None:
        if engine:
           self.backend=CirqBackend(engine)
        else:
            self.backend = simulator

    ############################### PUBLIC API ###############################
    @property
    def backend(self) -> Engine:
        return self._backend

    @backend.setter
    def backend(self, backend: Engine) -> None:
        validate_type(backend, Engine)
        self._backend: Engine = backend

    def create_circuit(self, num_qubits: int) -> CirqCircuit:
        return CirqCircuit(num_qubits)

    
    def create_job(  # type: ignore
        self,
        circuit: CirqCircuit,
        backend: CirqBackend,
        num_measurements: Optional[int] = None,
    ) -> CirqJob:
        return CirqJob(circuit,backend,num_measurements)


    def fetch_random_bits(self, protocol: QuantumProtocol) -> str:
        result: ProtocolResult = protocol.run(self)
        return result.bitstring


    ##Doubts
    def retrieve_backend(self) -> CirqBackend:
        return CirqBackend(self._backend)
