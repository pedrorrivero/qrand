##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: May 13, 2021
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
from typing import Optional


###############################################################################
## PROTOCOL RESULT INTERFACE
###############################################################################
class ProtocolResult(ABC):
    @property
    @abstractmethod
    def bitstring(self) -> str:
        pass

    @property
    @abstractmethod
    def validation_token(self) -> str:
        pass

    @abstractmethod
    def erase(self) -> None:
        pass


###############################################################################
## SIMPLE RESULT
###############################################################################
class PlainResult(ProtocolResult):
    def __init__(
        self, bitstring: str, validation_token: Optional[str] = None
    ) -> None:
        self._bitstring: str = bitstring
        self._validation_token: str = validation_token or bitstring

    ############################### PUBLIC API ###############################
    @property
    def bitstring(self) -> str:
        return self._bitstring

    @property
    def validation_token(self) -> str:
        return self._validation_token

    def erase(self) -> None:
        self._bitstring = ""
        self._validation_token = ""
