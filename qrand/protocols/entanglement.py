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

from ..platforms.factory import QuantumFactory
from .protocol import BareQuantumProtocol
from .result import ProtocolResult


###############################################################################
## ENTANGLEMENT PROTOCOL
###############################################################################
class EntanglementProtocol(BareQuantumProtocol):
    @property
    @classmethod
    def ERROR_MSG(cls):
        return f"{cls.__name__}"  # TODO

    ############################### PUBLIC API ###############################
    def run(
        self, factory: QuantumFactory, max_bits: Optional[int] = None
    ) -> ProtocolResult:
        raise NotImplementedError(self.__class__.ERROR_MSG)

    def verify(self) -> Literal[False]:
        raise NotImplementedError(self.__class__.ERROR_MSG)
