##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: May 26, 2021
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

import math
from struct import pack, unpack
from typing import Optional

from .errors import raise_future_warning
from .helpers import ALPHABETS, encode_numeral, validate_type
from .quantum_bit_generator import QuantumBitGenerator


###############################################################################
## QRNG (OBJECT WRAPPER)
###############################################################################
class Qrng:
    """
    A quantum random number generator.

    It extends the functionality of QRAND's QuantumBitGenerator class by
    wrapping it at the class level. Taking advantage of all its enhanced
    quantum random bit generation capabilities as well.

    Parameters
    ----------
    quantum_bit_generator: QuantumBitGenerator
        A QuantumBitGenerator instance object to handle random number
        production.

    Attributes
    ----------
    quantum_bit_generator: QuantumBitGenerator
        A QuantumBitGenerator instance object to handle random number
        production.

    Methods
    -------
    get_random_base32(num_bits: Optional[int] = None) -> str:
        Returns a random base32 encoded numeral string from a `num_bits`
        uniform distribution.
    get_random_base64(num_bits: Optional[int] = None) -> str:
        Returns a random base64 encoded numeral string from a `num_bits`
        uniform distribution.
    get_random_bitstring(num_bits: Optional[int] = None) -> str:
        Returns a random bitstring from a `num_bits` uniform distribution.
    get_random_bytes(num_bytes: Optional[int] = None) -> bytes:
        Returns a bytes object from a `num_bytes` uniform distribution.
    get_random_complex_polar(
        r: float = 1, theta: float = 2 * math.pi
    ) -> complex:
        Returns a random complex in rectangular form from a given polar range.
        If no max radius give, 1 is used. If no max angle given, 2pi used.
    get_random_complex_rect(
        r1: float = -1,
        r2: float = +1,
        i1: Optional[float] = None,
        i2: Optional[float] = None,
    ) -> complex:
        Returns a random complex with both real and imaginary parts from the
        given ranges. Default real range [-1,1). If no imaginary range
        specified, real range used.
    get_random_decimal(num_bits: Optional[int] = None) -> str:
        Returns a random decimal base encoded numeral string from a `num_bits`
        uniform distribution.
    get_random_double(min: float = -1, max: float = +1) -> float:
        Returns a random double from a uniform distribution in the range
        [min,max). Default range [-1,1).
    get_random_float(min: float = -1, max: float = +1) -> float:
        Returns a random float from a uniform distribution in the range
        [min,max). Default range [-1,1).
    get_random_hex(num_bits: Optional[int] = None) -> str:
        Returns a random hex base encoded numeral string from a `num_bits`
        uniform distribution.
    get_random_int(min: int = -1, max: int = +1) -> int:
        Returns a random integer between and including [min, max]. Default
        range [-1,1].
    get_random_int32() -> int:
        Returns a random 32 bit unsigned integer from a uniform distribution.
    get_random_int64() -> int:
        Returns a random 64 bit unsigned integer from a uniform distribution.
    get_random_octal(num_bits: Optional[int] = None) -> str:
        Returns a random octal base encoded numeral string from a `num_bits`
        uniform distribution.
    get_random_uint(num_bits: Optional[int] = None) -> int:
        Returns a random unsigned int from a `num_bits` uniform distribution.

    Notes
    -----
    COPYRIGHT ACKNOWLEDGEMENT
    Source: https://github.com/ozaner/qRNG/tree/v1.0.0
    License: GNU GENERAL PUBLIC LICENSE VERSION 3
    Changes:
        - Delete IBMQ log-in logic
        - Replace random bit generation and caching logic
        - Add default parameter values
        - Upgrade complex precision to double
        - Rename internal variables
        - Add static type hints
        - Fix endianness for bit manipulation.
        - Add additional features
    """

    def __init__(self, quantum_bit_generator: QuantumBitGenerator):
        raise_future_warning("This version of Qrng", "1.0.0")
        self.quantum_bit_generator = quantum_bit_generator

    ############################### PUBLIC API ###############################
    @property
    def quantum_bit_generator(self) -> QuantumBitGenerator:
        """
        A QuantumBitGenerator instance object to handle random number
        production.
        """
        raise_future_warning("quantum_bit_generator", "1.0.0")
        return self._quantum_bit_generator

    @quantum_bit_generator.setter
    def quantum_bit_generator(
        self, quantum_bit_generator: QuantumBitGenerator
    ) -> None:
        raise_future_warning("quantum_bit_generator", "1.0.0")
        validate_type(quantum_bit_generator, QuantumBitGenerator)
        self._quantum_bit_generator: QuantumBitGenerator = (
            quantum_bit_generator
        )

    @property
    def state(self) -> dict:
        """
        The state of the Qrng object.
        """
        raise_future_warning("state", "1.0.0")
        return {
            "quantum_bit_generator": self.quantum_bit_generator.state,
        }

    def get_bit_string(self, num_bits: Optional[int] = None) -> str:
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
        raise_future_warning("get_bit_string", "1.0.0", "get_random_bitstring")
        return self.quantum_bit_generator.random_bitstring(num_bits)

    def get_random_base32(self, num_bits: Optional[int] = None) -> str:
        """
        Returns a random base32 encoded numeral string from a `num_bits`
        uniform distribution.

        Parameters
        ----------
        num_bits: int, default: BITS (i.e. 32 or 64)
            Number of bits to retrieve.

        Returns
        -------
        out: str
            Random base32 encoded numeral string.
        """
        uint: int = self.get_random_uint(num_bits)
        return encode_numeral(uint, ALPHABETS["BASE32"])

    def get_random_base64(self, num_bits: Optional[int] = None) -> str:
        """
        Returns a random base64 encoded numeral string from a `num_bits`
        uniform distribution.

        Parameters
        ----------
        num_bits: int, default: BITS (i.e. 32 or 64)
            Number of bits to retrieve.

        Returns
        -------
        out: str
            Random base64 encoded numeral string.
        """
        uint: int = self.get_random_uint(num_bits)
        return encode_numeral(uint, ALPHABETS["BASE64"])

    def get_random_bitstring(self, num_bits: Optional[int] = None) -> str:
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
        return self.quantum_bit_generator.random_bitstring(num_bits)

    def get_random_bytes(self, num_bytes: Optional[int] = None) -> bytes:
        """
        Returns a bytes object from a `num_bytes` uniform distribution.

        Parameters
        ----------
        num_bytes: int, default: BITS/8 (i.e. 4 or 8)
            Number of bytes to randomly produce.

        Returns
        -------
        out: bytes
            Random bytes object of size `num_bytes`.
        """
        num_bits: int = (
            num_bytes * 8
            if num_bytes and type(num_bytes) is int and num_bytes > 0
            else self.quantum_bit_generator.BITS
        )
        num_bytes = num_bits // 8
        uint: int = self.quantum_bit_generator.random_uint(num_bits)
        return uint.to_bytes(num_bytes, "big")

    def get_random_complex_polar(
        self, r: float = 1, theta: float = 2 * math.pi
    ) -> complex:
        """
        Returns a random complex in rectangular form from a given polar range.
        If no max radius give, 1 is used. If no max angle given, 2pi used.

        Parameters
        ----------
        r: float, default 1
            Real lower bound for the random number.
        theta: float, default 2pi
            Real strict upper bound for the random number.

        Returns
        -------
        out: complex
            Random complex in the range [0,r) * exp{ j[0,theta) }.
        """
        r0: float = r * math.sqrt(self.get_random_double(0, 1))
        theta0: float = self.get_random_double(0, theta)
        return r0 * math.cos(theta0) + r0 * math.sin(theta0) * 1j

    def get_random_complex_rect(
        self,
        r1: float = -1,
        r2: float = +1,
        i1: Optional[float] = None,
        i2: Optional[float] = None,
    ) -> complex:
        """
        Returns a random complex with both real and imaginary parts from the
        given ranges. Default real range [-1,1). If no imaginary range
        specified, real range used.

        Parameters
        ----------
        r1: float, default -1
            Real lower bound for the random number.
        r2: float, default +1
            Real strict upper bound for the random number.
        i1: float, default None
            Imaginary lower bound for the random number.
        i2: float, default None
            Imaginary strict upper bound for the random number.

        Returns
        -------
        out: complex
            Random complex in the range [r1,r2) + j[i1,i2).
        """
        re: float = self.get_random_double(r1, r2)
        if i1 is None or i2 is None:
            im: float = self.get_random_double(r1, r2)
        else:
            im = self.get_random_double(i1, i2)
        return re + im * 1j

    def get_random_decimal(self, num_bits: Optional[int] = None) -> str:
        """
        Returns a random decimal base encoded numeral string from a `num_bits`
        uniform distribution.

        Parameters
        ----------
        num_bits: int, default: BITS (i.e. 32 or 64)
            Number of bits to retrieve.

        Returns
        -------
        out: str
            Random decimal base encoded numeral string.
        """
        uint: int = self.quantum_bit_generator.random_uint(num_bits)
        return f"{uint:d}"

    def get_random_double(self, min: float = -1, max: float = +1) -> float:
        """
        Returns a random double from a uniform distribution in the range
        [min,max). Default range [-1,1).

        Parameters
        ----------
        min: float, default -1
            Lower bound for the random number.
        max: float, default +1
            Strict upper bound for the random number.

        Returns
        -------
        out: float
            Random float in the range [min,max).
        """
        min, max = float(min), float(max)
        delta: float = max - min
        shifted: float = self.quantum_bit_generator.random_double(delta)
        return shifted + min

    def get_random_float(self, min: float = -1, max: float = +1) -> float:
        """
        Returns a random float from a uniform distribution in the range
        [min,max). Default range [-1,1).

        Parameters
        ----------
        min: float, default -1
            Lower bound for the random number.
        max: float, default +1
            Strict upper bound for the random number.

        Returns
        -------
        out: float
            Random float in the range [min,max).

        Notes
        -----
        Implementation based on the single-precision floating-point format
        (FP32) [1]_.

        References
        ----------
        .. [1] Wikipedia contributors, "Single-precision floating-point
            format," Wikipedia, The Free Encyclopedia,
            https://en.wikipedia.org/w/index.php?title=
            Single-precision_floating-point_format&oldid=1024960263
            (accessed May 25, 2021).
        """
        min, max = float(min), float(max)
        bits_as_uint: int = (
            0x3F800000 | self.quantum_bit_generator.random_uint(32 - 9)
        )
        to_bytes: bytes = pack(">I", bits_as_uint)
        standard_value: float = unpack(">f", to_bytes)[0] - 1.0
        return (max - min) * standard_value + min

    def get_random_hex(self, num_bits: Optional[int] = None) -> str:
        """
        Returns a random hex base encoded numeral string from a `num_bits`
        uniform distribution.

        Parameters
        ----------
        num_bits: int, default: BITS (i.e. 32 or 64)
            Number of bits to retrieve.

        Returns
        -------
        out: str
            Random hex base encoded numeral string.
        """
        uint: int = self.quantum_bit_generator.random_uint(num_bits)
        return f"{uint:X}"

    def get_random_int(self, min: int = -1, max: int = +1) -> int:
        """
        Returns a random integer between and including [min, max]. Default
        range [-1,1].

        Parameters
        ----------
        min: int, default -1
            Lower bound for the random int.
        max: int, default +1
            Upper bound for the random int.

        Returns
        -------
        out: int
            Random int in the range [min,max].
        """
        delta: int = max - min
        num_bits: int = math.floor(math.log(delta, 2)) + 1
        shifted: int = self.quantum_bit_generator.random_uint(num_bits)
        while shifted > delta:
            shifted = self.quantum_bit_generator.random_uint(num_bits)
        return shifted + min

    def get_random_int32(self) -> int:
        """
        Returns a random 32 bit unsigned integer from a uniform distribution.

        Returns
        -------
        out: int
            Random 32 bit unsigned int.
        """
        return self.quantum_bit_generator.random_uint(32)

    def get_random_int64(self) -> int:
        """
        Returns a random 64 bit unsigned integer from a uniform distribution.

        Returns
        -------
        out: int
            Random 64 bit unsigned int.
        """
        return self.quantum_bit_generator.random_uint(64)

    def get_random_octal(self, num_bits: Optional[int] = None) -> str:
        """
        Returns a random octal base encoded numeral string from a `num_bits`
        uniform distribution.

        Parameters
        ----------
        num_bits: int, default: BITS (i.e. 32 or 64)
            Number of bits to retrieve.

        Returns
        -------
        out: str
            Random octal base encoded numeral string.
        """
        uint: int = self.quantum_bit_generator.random_uint(num_bits)
        return f"{uint:o}"

    def get_random_uint(self, num_bits: Optional[int] = None) -> int:
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
        return self.quantum_bit_generator.random_uint(num_bits)
