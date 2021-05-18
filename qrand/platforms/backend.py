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

from ..helpers import compute_bounded_factorization


###############################################################################
## QUANTUM BACKEND BASE INTERFACE (ADAPTER)
###############################################################################
class QuantumBackend(ABC):
    ################################ ABSTRACT ################################
    @property
    @abstractmethod
    def max_measurements(self) -> int:
        pass

    @property
    @abstractmethod
    def max_qubits(self) -> int:
        pass

    ################################ CONCRETE ################################
    @property
    def job_partition(self) -> Tuple[int, int]:
        return compute_bounded_factorization(
            self.max_bits_per_request, self.max_qubits, self.max_measurements
        )

    @property
    def max_bits_per_request(self) -> int:
        try:
            mbpr = self._max_bits_per_request
        except AttributeError:
            mbpr = None
        max_allowed: int = self.max_qubits * self.max_measurements
        return mbpr if mbpr and 0 < mbpr < max_allowed else max_allowed

    @max_bits_per_request.setter
    def max_bits_per_request(self, mbpr: Optional[int]) -> None:
        mbpr = mbpr or 0
        if not isinstance(mbpr, int):
            raise TypeError(f"Expected int instance, {type(mbpr)} found")
        self._max_bits_per_request: Optional[int] = mbpr if mbpr > 0 else None
