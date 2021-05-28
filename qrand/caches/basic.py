##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: May 28, 2021
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

from ..errors import raise_future_warning
from ..helpers import ALPHABETS, validate_natural_number, validate_numeral
from .cache import BitCache


###############################################################################
## BASIC CACHE
###############################################################################
class BasicCache(BitCache):
    """
    Basic non-persistent implementation of the BitCache FIFO data structure.

    Attributes
    ----------
    size: int
        The number of bits currently stored in the BitCache.

    Methods
    -------
    dump() -> str
        Outputs all the contents in the cache without erasing.
    flush() -> None:
        Erases the cache.
    pop(n: int) -> str:
        Returns a size `n` bitstring removing it from the top of the cache.
    push(bitstring: str) -> None:
        Inserts bitstring at the end of the cache.
    """

    def __init__(self) -> None:
        self._cache: str = ""

    ############################### PUBLIC API ###############################
    @property
    def size(self) -> int:
        return len(self._cache)

    @property
    def state(self) -> dict:
        """
        The state of the BitCache object.
        """
        raise_future_warning("state", "1.0.0")
        return {"size": self.size}

    def dump(self) -> str:
        return self._cache

    def flush(self) -> None:
        self._cache = ""

    def pop(self, num_bits: int) -> str:
        validate_natural_number(num_bits, zero=False)
        if num_bits > self.size:
            raise RuntimeError(
                f"Insufficient cache size {self.size} < {num_bits}."
            )
        bitstring: str = self._cache[:num_bits]
        self._cache = self._cache[num_bits:]
        return bitstring

    def push(self, bitstring: str) -> None:
        validate_numeral(bitstring, ALPHABETS["BINARY"])
        self._cache += bitstring
