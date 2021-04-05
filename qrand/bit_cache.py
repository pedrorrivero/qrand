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

###############################################################################
## BIT CACHE
###############################################################################
class BitCache:
    """
    BitCache first in, first out (FIFO) data structure.
    """

    def __init__(self) -> None:
        self._cache: str = ""
        self.size: int = 0

    ########################## STATIC/CLASS METHODS ##########################
    @staticmethod
    def isbitstring(bitstring: str) -> bool:
        """
        Returns `True` if the input str is a bitstring, `False` otherwise.

        PARAMETERS
        ----------
        bitstring: str
            The string to check.

        RETURNS
        -------
        out: bool
            `True` if input str is bitstring, `False` otherwise.

        RAISES
        ------
        TypeError
            If input bitstring is not str.
        """
        if not isinstance(bitstring, str):
            raise TypeError(f"Invalid bitstring type '{type(bitstring)}'")
        b = {"0", "1"}
        s = set(bitstring)
        return s.issubset(b)

    ############################# PUBLIC METHODS #############################
    def dump(self) -> str:
        """
        Outputs all the contents in the cache without erasing.

        RETURNS
        -------
        out: str
            Cache contents.
        """
        return self._cache

    def flush(self) -> bool:
        """
        Erases the cache.

        RETURNS
        -------
        out: bool
            `True` if succeeds, `False` otherwise.
        """
        self._cache = ""
        self.size = 0
        return True

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
            raise ValueError("Insufficient cache size")
        bitstring: str = self._cache[:n]
        self._cache = self._cache[n:]
        self.size -= n if n < self.size else self.size
        return bitstring

    def push(self, bitstring: str) -> bool:
        """
        Inserts bitstring at the end of the cache.

        PARAMETERS
        ----------
        bitstring: str
            The bitstring to insert.

        RETURNS
        -------
        out: bool
            `True` if succeeds, `False` otherwise.

        RAISES
        ------
        TypeError (isbitstring)
            If input bitstring is not str
        ValueError
            If input bitstring is not a valid bitstring
        """
        if not BitCache.isbitstring(bitstring):
            raise ValueError(f"Invalid bitstring value '{bitstring}'")
        self._cache += bitstring
        self.size += len(bitstring)
        return True

    ############################ PUBLIC PROPERTIES ############################
    @property
    def state(self) -> dict:
        """
        The state of the BitCache object.
        """
        return {"size": self.size}
