##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: May 12, 2021
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

from struct import pack, unpack
from typing import Any, Callable, Final, Union

from numpy import float64, uint32, uint64
from randomgen import UserBitGenerator

from .bit_cache import BitCache
from .platforms import QuantumPlatform
from .protocols import QuantumProtocol


###############################################################################
## QUANTUM BIT GENERATOR (FACADE)
###############################################################################
class QuantumBitGenerator(UserBitGenerator):
    def __init__(
        self,
        platform: QuantumPlatform,
        protocol: QuantumProtocol,
        ISRAW32: bool = False,
    ) -> None:
        self.platform: QuantumPlatform = platform
        self.protocol: QuantumProtocol = protocol
        self._ISRAW32: Final[bool] = ISRAW32
        self._bitcache: BitCache = BitCache()
        super().__init__(
            bits=self.BITS,
            next_raw=self._next_raw,
            next_32=self._next_32,
            next_64=self._next_64,
            next_double=self._next_double,
        )

    ############################### PUBLIC API ###############################
    @property
    def BITS(self) -> int:
        """
        Either 32 or 64. The number of bits output by NumPy's `random_raw()`
        method. Final, it cannot be modified after instantiation through the
        ISRAW32 parameter.
        """
        return 32 if self._ISRAW32 else 64

    @property
    def platform(self) -> QuantumPlatform:
        return self._platform

    @platform.setter
    def platform(self, p: QuantumPlatform) -> None:
        self._platform = p

    @property
    def protocol(self) -> QuantumProtocol:
        return self._protocol

    @protocol.setter
    def protocol(self, p: QuantumProtocol) -> None:
        self._protocol = p

    def dump_cache(self, flush: bool = False) -> str:
        """
        Returns all the contents stored in the cache.

        PARAMETERS
        ----------
        flush: bool
            If `True` erase the cache after dumping.

        RETURNS
        -------
        out: str
            The bitstring stored in cache.
        """
        bitstring: str = self._bitcache.dump()
        if flush:
            self._bitcache.flush()
        return bitstring

    def flush_cache(self) -> None:
        """
        Erase the cache.

        RETURNS
        -------
        out: bool
            `True` if succeeds, `False` otherwise.
        """
        self._bitcache.flush()

    def load_cache(self, bitstring: str, flush: bool = False) -> None:
        """
        Load cache contents from bitstring.

        PARAMETERS
        ----------
        bitstring: str
            The bitstring to load to cache.
        flush: bool
            If `True` erase cache before loading.

        RETURNS
        -------
        out: bool
            `True` if succeeds, `False` otherwise.

        RAISES
        ------
        TypeError (push)
            If input bitstring is not str
        ValueError (push)
            If input bitstring is not a valid bitstring
        """
        if flush:
            self._bitcache.flush()
        self._bitcache.push(bitstring)

    def random_bitstring(self, num_bits: int = 0) -> str:
        """
        Returns a random bitstring of a given lenght. If less than one it
        defaults to the raw number of bits for the instance QiskitBitGenerator
        (i.e. 32 or 64).

        PARAMETERS
        ----------
        num_bits: int
            Number of bits to retrieve.

        RETURNS
        -------
        out: str
            Bitstring of lenght `num_bits`.
        """
        if num_bits < 1:
            num_bits = self.BITS
        while self._bitcache.size < num_bits:
            self._refill_cache()
        return self._bitcache.pop(num_bits)

    def random_double(self, n: float = 1) -> float:
        """
        Returns a random double from a uniform distribution in the range
        [0,n). Defaults to [0,1).

        PARAMETERS
        ----------
        n: float
            Size of the range [0,n) from which to draw the random number.

        RETURNS
        -------
        out: float
            Random float in the range [0,n).

        COPYRIGHT NOTICE
        ----------------
        Source: https://github.com/ozanerhansha/qRNG
        License: GNU GENERAL PUBLIC LICENSE VERSION 3
        Changes:
            - Add static type hints
            - Limit range to [0,n) instead of [min,max) and add default
            - Replace call to original get_random_int64
        """
        unpacked = 0x3FF0000000000000 | self.random_uint(64) >> 12
        packed = pack("Q", unpacked)
        value: float = unpack("d", packed)[0] - 1.0
        return value * n

    def random_uint(self, num_bits: int = 0) -> int:
        """
        Returns a random unsigned int of a given size in bits.

        PARAMETERS
        ----------
        num_bits: int
            Number of bits to retrieve. If less than one it defaults to the raw
            number of bits for the instance QiskitBitGenerator (i.e. 32 or 64).

        RETURNS
        -------
        out: int
            Unsigned int of `num_bits` bits.
        """
        if num_bits < 1:
            num_bits = self.BITS
        return int(self.random_bitstring(num_bits), 2)

    ############################### PRIVATE API ###############################
    def _refill_cache(self) -> None:
        bitstring: str = self.platform.fetch_random_bits(self.protocol)
        self._bitcache.push(bitstring)

    ############################# NUMPY INTERFACE #############################
    @property
    def _next_raw(self) -> Callable[[Any], Union[uint32, uint64]]:
        """
        A callable that returns either 64 or 32 random bits. It must accept
        a single input which is a void pointer to a memory address.
        """
        return self._next_32 if self._ISRAW32 else self._next_64

    @property
    def _next_32(self) -> Callable[[Any], uint32]:
        """
        A callable with the same signature as as next_raw that always returns
        a random numpy 32-bit unsigned int.
        """

        def next_32(void_p: Any) -> uint32:
            return uint32(self.random_uint(32))

        return next_32

    @property
    def _next_64(self) -> Callable[[Any], uint64]:
        """
        A callable with the same signature as as next_raw that always returns
        a random numpy 64-bit unsigned int.
        """

        def next_64(void_p: Any) -> uint64:
            return uint64(self.random_uint(64))

        return next_64

    @property
    def _next_double(self) -> Callable[[Any], float64]:
        """
        A callable with the same signature as as next_raw that always return
        a random double in [0,1).
        """

        def next_double(void_p: Any) -> float64:
            return float64(self.random_double(1))

        return next_double
