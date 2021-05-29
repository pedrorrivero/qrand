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

from typing import Optional

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
        self.resource_id = resource_id
        self.target_id = target_id

    ############################### PUBLIC API ###############################
    @property
    def max_measurements(self) -> int:
        return 524288

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
            return 1
