##    _____  _____
##   |  __ \|  __ \    AUTHOR: A. Nair, P. Rivero
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

from ...helpers import validate_type
from ..backend import QuantumBackend


###############################################################################
## QSHARP BACKEND (DECORATOR)
###############################################################################
class QsharpBackend(QuantumBackend):
    def __init__(
        self,
        resource_id: Optional[str] = None,
        target_id: Optional[str] = None,
    ) -> None:
        self.resource_id: Optional[str] = resource_id
        self.target_id: Optional[str] = target_id

    ############################### PUBLIC API ###############################
    @property
    def resource_id(self) -> Optional[str]:
        return self._resource_id

    @resource_id.setter
    def resource_id(self, resource_id: Optional[str]) -> None:
        validate_type(resource_id, (str, type(None)))
        self._resource_id: Optional[str] = resource_id

    @property
    def target_id(self) -> Optional[str]:
        return self._target_id

    @target_id.setter
    def target_id(self, target_id: Optional[str]) -> None:
        validate_type(target_id, (str, type(None)))
        self._target_id: Optional[str] = target_id

    @property
    def max_measurements(self) -> int:
        return 1048576  # TODO!! (Q# truly does not have any max_measurements)

    @property
    def max_qubits(self) -> int:
        if self.target_id == "ionq.simulator":
            return 29
        elif self.target_id == "ionq.qpu":
            return 11
        elif self.target_id == "honeywell.hqs-lt-1.0":
            return 6
        elif self.target_id == "honeywell.hqs-lt-s1":
            return 10
        else:
            return 30
