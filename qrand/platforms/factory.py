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

from abc import ABC, abstractmethod
from typing import Optional, Tuple

from .backend import QuantumBackend
from .circuit import QuantumCircuit
from .job import QuantumJob


###############################################################################
## QUANTUM PLATFORM BASE INTERFACE (ABSTRACT FACTORY)
###############################################################################
class QuantumFactory(ABC):
    @abstractmethod
    def create_circuit(self, num_qubits: int) -> QuantumCircuit:
        pass

    @abstractmethod
    def create_job(
        self,
        circuit: QuantumCircuit,
        backend: QuantumBackend,
        num_measurements: Optional[int] = None,
    ) -> QuantumJob:
        pass

    @abstractmethod
    def retrieve_backend(
        self, max_bits_per_request: Optional[int] = None
    ) -> QuantumBackend:
        pass
