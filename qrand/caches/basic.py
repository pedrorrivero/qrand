##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: May 18, 2021
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

from ..errors import raise_deprecation_warning
from ..helpers import is_bitstring
from .cache import BitCache


###############################################################################
## BASIC CACHE
###############################################################################
class BasicCache(BitCache):
    """
    BitCache first in, first out (FIFO) data structure.
    """

    def __init__(self) -> None:
        self._cache: str = ""

    ############################### PUBLIC API ###############################
    @property
    def size(self) -> int:
        """
        The number of bits currently stored in the BitCache.
        """
        return len(self._cache)

    @property
    def state(self) -> dict:
        """
        The state of the BitCache object.
        """
        raise_deprecation_warning("state", "1.0.0")
        return {"size": self.size}

    def dump(self) -> str:
        """
        Outputs all the contents in the cache without erasing.

        RETURNS
        -------
        out: str
            Cache contents.
        """
        return self._cache

    def flush(self) -> None:
        """
        Erases the cache.
        """
        self._cache = ""

    def pop(self, n: int) -> str:
        """
        Returns a size `n` bitstring removing it from the top of the cache.

        PARAMETERS
        ----------
        n: int
            Number of bits to retrieve

        RETURNS
        -------
        out: str
            Size `n` bitstring.

        RAISES
        ------
        ValueError
            If input is greater than cache size, or less than one.
        """
        if n < 1:
            raise ValueError("Input number of bits must be greater than zero")
        elif n > self.size:
            raise RuntimeError("Insufficient cache size")
        bitstring: str = self._cache[:n]
        self._cache = self._cache[n:]
        return bitstring

    def push(self, bitstring: str) -> None:
        """
        Inserts bitstring at the end of the cache.

        PARAMETERS
        ----------
        bitstring: str
            The bitstring to insert.

        RAISES
        ------
        TypeError (is_bitstring)
            If input bitstring is not str
        ValueError
            If input bitstring is not a valid bitstring
        """
        if not is_bitstring(bitstring):
            raise ValueError(f"Invalid bitstring value '{bitstring}'")
        self._cache += bitstring
