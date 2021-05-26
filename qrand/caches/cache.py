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

from abc import ABC, abstractmethod

from ..helpers import isbitstring


###############################################################################
## BIT CACHE INTERFACE
###############################################################################
class BitCache(ABC):
    """
    BitCache first in, first out (FIFO) data structure.
    """

    ############################### PUBLIC API ###############################
    @property
    @abstractmethod
    def size(self) -> int:
        """
        The number of bits currently stored in the BitCache.
        """
        pass

    @abstractmethod
    def dump(self) -> str:
        """
        Outputs all the contents in the cache without erasing.

        RETURNS
        -------
        out: str
            Cache contents.
        """
        pass

    @abstractmethod
    def flush(self) -> None:
        """
        Erases the cache.
        """
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    def push(self, bitstring: str) -> None:
        """
        Inserts bitstring at the end of the cache.

        PARAMETERS
        ----------
        bitstring: str
            The bitstring to insert.

        RAISES
        ------
        TypeError (isbitstring)
            If input bitstring is not str
        ValueError
            If input bitstring is not a valid bitstring
        """
        pass
