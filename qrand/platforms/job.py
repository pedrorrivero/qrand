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
from typing import List, Optional

from .backend import QuantumBackend
from .circuit import QuantumCircuit


###############################################################################
## QUANTUM JOB INTERFACE (ADAPTER)
###############################################################################
class QuantumJob(ABC):
    @property
    @abstractmethod
    def backend(self) -> QuantumBackend:
        pass

    @backend.setter
    def backend(self, backend: QuantumBackend) -> None:
        pass

    @property
    @abstractmethod
    def circuit(self) -> QuantumCircuit:
        pass

    @circuit.setter
    def circuit(self, circuit: QuantumCircuit) -> None:
        pass

    @property
    @abstractmethod
    def num_measurements(self) -> int:
        pass

    @num_measurements.setter
    def num_measurements(self, num_measurements: Optional[int]) -> None:
        pass

    @abstractmethod
    def execute(self) -> List[str]:
        pass
