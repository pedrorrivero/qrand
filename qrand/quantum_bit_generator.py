##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: May 25, 2021
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
from typing import Any, Callable, Final, Optional, Union

from numpy import float64, uint32, uint64
from randomgen import UserBitGenerator

from .bitcaches import BasicCache, BitCache
from .helpers import validate_type
from .platforms import QuantumPlatform
from .protocols import HadamardProtocol, QuantumProtocol


###############################################################################
## QUANTUM BIT GENERATOR (FACADE)
###############################################################################
class QuantumBitGenerator(UserBitGenerator):
    """
    A quantum random bit-generator which can interface with NumPy's random
    module.

    Parameters
    ----------
    platform: QuantumPlatform
        The quantum platform that will be used for QRNG.
    protocol: QuantumProtocol, default: HadamardProtocol()
        The quantum protocol that will be used for QRNG.
    ISRAW32: bool, default: False
        Toggle 32-bit BitGenerator mode. If `False` the mode will be 64-bit.
        This determines the default number of output BITS. Final: once an
        object is instantiated, it cannot be overridden.

    Attributes
    ----------
    BITS: int
        The default number of output bits: either 32 or 64.
    bitcache: BitCache
        The cache to store retrieved random bits.
    platform: QuantumPlatform
        The quantum platform used for QRNG.
    protocol: QuantumProtocol
        The quantum protocol used for QRNG.

    Methods
    -------
    dump_cache(flush: bool = False) -> str
        Returns all the contents stored in the cache.
    flush_cache() -> None:
        Erase the cache.
    load_cache(bitstring: str, flush: bool = False) -> None:
        Load cache from bitstring.
    random_bitstring(num_bits: Optional[int] = None) -> str:
        Returns a random bitstring of a given lenght.
    random_double(max: float = 1, min: float = 0) -> float:
        Returns a random double from a uniform distribution in the range [0,n).
    random_uint(num_bits: Optional[int] = None) -> int:
        Returns a random unsigned int of a given size in bits.

    Notes
    -----
    It implements an efficient strategy to retrieve random bits from the cloud
    quantum backends. Namely, on every conection, it retrieves as many bits as
    possible and stores them in a cache. This way, the total number of internet
    connections is greatly reduced.
    """

    def __init__(
        self,
        platform: QuantumPlatform,
        protocol: QuantumProtocol = HadamardProtocol(),
        ISRAW32: bool = False,
    ) -> None:
        self.platform: QuantumPlatform = platform
        self.protocol: QuantumProtocol = protocol
        self._ISRAW32: Final[bool] = ISRAW32
        self._bitcache: BitCache = self._build_cache()
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
        The default number of output bits: either 32 or 64.

        Final: it cannot be modified after instantiation through the ISRAW32
        parameter. This is required by NumPy (e.g. `random_raw()` method).
        """
        return 32 if self._ISRAW32 else 64

    @property
    def bitcache(self) -> BitCache:
        """
        The cache to store retrieved random bits.
        """
        return self._bitcache

    @property
    def platform(self) -> QuantumPlatform:
        """
        The quantum platform used for QRNG.
        """
        return self._platform

    @platform.setter
    def platform(self, p: QuantumPlatform) -> None:
        validate_type(p, QuantumPlatform)
        self._platform = p

    @property
    def protocol(self) -> QuantumProtocol:
        """
        The quantum protocol used for QRNG.
        """
        return self._protocol

    @protocol.setter
    def protocol(self, p: QuantumProtocol) -> None:
        validate_type(p, QuantumProtocol)
        self._protocol = p

    def dump_cache(self, flush: bool = False) -> str:
        """
        Returns all the contents stored in the cache.

        Parameters
        ----------
        flush: bool, default: False
            If `True` erase the cache after dumping.

        Returns
        -------
        out: str
            The complete bitstring stored in cache.
        """
        bitstring: str = self.bitcache.dump()
        if flush:
            self.bitcache.flush()
        return bitstring

    def flush_cache(self) -> None:
        """
        Erase the cache.
        """
        self.bitcache.flush()

    def load_cache(self, bitstring: str, flush: bool = False) -> None:
        """
        Load cache from bitstring.

        Parameters
        ----------
        bitstring: str
            The bitstring to load to cache.
        flush: bool, default: False
            If `True` erase cache before loading.
        """
        if flush:
            self.bitcache.flush()
        self.bitcache.push(bitstring)

    def random_bitstring(self, num_bits: Optional[int] = None) -> str:
        """
        Returns a random bitstring from a `num_bits` uniform distribution.

        Parameters
        ----------
        num_bits: int, default: BITS (i.e. 32 or 64)
            Number of bits to retrieve.

        Returns
        -------
        out: str
            Random bitstring of length `num_bits`.
        """
        num_bits = (
            num_bits
            if isinstance(num_bits, int) and num_bits > 0
            else self.BITS
        )
        while self.bitcache.size < num_bits:
            self._refill_cache()
        return self.bitcache.pop(num_bits)

    def random_double(self, max: float = 1, min: float = 0) -> float:
        """
        Returns a random double from a uniform distribution in the range
        [min,max).

        Parameters
        ----------
        max: float, default: 1
            Strict upper bound for the random number.
        min: float, default: 0
            Lower bound for the random number.

        Returns
        -------
        out: float
            Random double in the range [min,max).

        Notes
        -----
        Implementation based on the double-precision floating-point format
        (FP64) [1]_.

        References
        ----------
        .. [1] Wikipedia contributors, "Double-precision floating-point
            format," Wikipedia, The Free Encyclopedia,
            https://en.wikipedia.org/w/index.php?title=
            Double-precision_floating-point_format&oldid=1024750735
            (accessed May 25, 2021).
        """
        min, max = float(min), float(max)
        bits_as_uint: int = 0x3FF0000000000000 | self.random_uint(64 - 12)
        to_bytes: bytes = pack(">Q", bits_as_uint)
        standard_value: float = unpack(">d", to_bytes)[0] - 1.0
        return (max - min) * standard_value + min

    def random_uint(self, num_bits: Optional[int] = None) -> int:
        """
        Returns a random unsigned int from a `num_bits` uniform distribution.

        Parameters
        ----------
        num_bits: int, default: BITS (i.e. 32 or 64)
            Number of bits to retrieve.

        Returns
        -------
        out: int
            Random unsigned int of size `num_bits`.
        """
        return int(self.random_bitstring(num_bits), base=2)

    ############################### PRIVATE API ###############################
    def _build_cache(self) -> BitCache:
        """
        Build new BitCache.

        Returns
        -------
        out: BitCache
            New BasicCache instance.
        """
        return BasicCache()

    def _refill_cache(self) -> None:
        """
        Refill cache by fetching new random bits.
        """
        bitstring: str = self.platform.fetch_random_bits(self.protocol)
        if not bitstring:
            raise RuntimeError("Failed to fetch random bits.")
        self.bitcache.push(bitstring)

    ############################# NUMPY INTERFACE #############################
    @property
    def _next_raw(self) -> Callable[[Any], Union[uint32, uint64]]:
        """
        A callable that returns either 64 or 32 random bits. It must accept a
        single input which is a void pointer to a memory address.
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
            return float64(self.random_double(1, 0))

        return next_double
