##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: April 5, 2021
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
import math

###############################################################################
## VALIDATION STRATEGY INTERFACE (STRATEGY)
###############################################################################
class ValidationStrategy(ABC):
    @abstractmethod
    def validate(self, bitstring: str) -> bool:
        pass


class FrequencyTest(ValidationStrategy):
    def validate(self, bitstring: str) -> bool:
        n = len(bitstring)
        s_obs = 0
        for bit in bitstring:
            s_obs += 2 * int(bit) - 1
        s_obs = s_obs / math.sqrt(n)
        p_value = math.erfc(s_obs / math.sqrt(2))
        return p_value > 0.01
