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
from typing import Literal, Optional

from ..platforms.factory import QuantumFactory
from ..validation import ValidationStrategy
from .result import ProtocolResult


###############################################################################
## QUANTUM PROTOCOL INTERFACE (STRATEGY AND DECORATOR)
###############################################################################
class QuantumProtocol(ABC):
    ############################ STRATEGY PATTERN ############################
    @abstractmethod
    def run(
        self, factory: QuantumFactory, max_bits: Optional[int] = None
    ) -> ProtocolResult:
        pass

    @abstractmethod
    def verify(self) -> bool:
        pass

    ############################ DECORATOR PATTERN ############################
    @property
    @abstractmethod
    def base_protocol(self) -> Optional["QuantumProtocol"]:
        pass

    @abstractmethod
    def validate(self, result: ProtocolResult) -> bool:
        pass


###############################################################################
## BASE QUANTUM PROTOCOL INTERFACE
###############################################################################
class BareQuantumProtocol(QuantumProtocol):
    ############################ STRATEGY PATTERN ############################
    @abstractmethod
    def run(
        self, factory: QuantumFactory, max_bits: Optional[int] = None
    ) -> ProtocolResult:
        pass

    @abstractmethod
    def verify(self) -> bool:
        pass

    ############################ DECORATOR PATTERN ############################
    @property
    def base_protocol(self) -> Literal[None]:
        return None

    def validate(self, result: ProtocolResult) -> Literal[False]:
        return False


###############################################################################
## VALIDATION DECORATOR
###############################################################################
class ValidationDecorator(QuantumProtocol):
    def __init__(
        self,
        base_protocol: QuantumProtocol,
        validation_strategy: ValidationStrategy,
    ) -> None:
        self.base_protocol: QuantumProtocol = base_protocol
        self.validation_strategy: ValidationStrategy = validation_strategy

    ############################ STRATEGY PATTERN ############################
    def run(
        self, factory: QuantumFactory, max_bits: Optional[int] = None
    ) -> ProtocolResult:
        result: ProtocolResult = self.base_protocol.run(factory, max_bits)
        if not self._validate_layer(result):
            result.erase()
        return result

    def verify(self) -> bool:
        return self.base_protocol.verify()

    ############################ DECORATOR PATTERN ############################
    @property
    def base_protocol(self) -> QuantumProtocol:
        return self._base_protocol

    @base_protocol.setter
    def base_protocol(self, protocol: QuantumProtocol) -> None:
        self._base_protocol: QuantumProtocol = protocol

    def validate(self, result: ProtocolResult) -> bool:
        valid: bool = self._validate_layer(result)
        if self.base_protocol.base_protocol is None:
            return valid
        return valid and self.base_protocol.validate(result)

    ############################### PUBLIC API ###############################
    @property
    def validation_strategy(self) -> ValidationStrategy:
        return self._validation_strategy

    @validation_strategy.setter
    def validation_strategy(self, strategy: ValidationStrategy) -> None:
        self._validation_strategy: ValidationStrategy = strategy

    ############################### PRIVATE API ###############################
    def _validate_layer(self, result: ProtocolResult) -> bool:
        validation_token: str = result.validation_token
        return self._validation_strategy.validate(validation_token)
