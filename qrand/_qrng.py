##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: February 23, 2021
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
import struct
from typing import Optional

from ._qiskit_bit_generator import QiskitBitGenerator


###############################################################################
## QRNG
###############################################################################
class Qrng:
    """
    An integrated implementation of the QRNG PyPI package which makes use of
    QRAND's enhanced random bit generation and caching capabilities.

    PARAMETERS
    ----------
    qiskit_bit_generator: QiskitBitGenerator
        A QiskitBitGenerator instance object to handle random number production.

    COPYRIGHT NOTICE
    ----------------
    Source: https://github.com/ozanerhansha/qRNG
    License: GNU GENERAL PUBLIC LICENSE VERSION 3
    Changes:
        - Delete IBMQ log-in logic
        - Replace random bit generation and caching logic
        - Add static type hints
        - Rename internal variables
    """

    def __init__(self, qiskit_bit_generator: QiskitBitGenerator):
        self._qiskit_bit_generator = qiskit_bit_generator

    ############################# PUBLIC METHODS #############################
    def get_bit_string(self, n_bits: int):
        """
        Returns a random bitstring of a given lenght.

        PARAMETERS
        ----------
        n_bits: int
            Number of bits to retrieve. If less than one it defaults to the raw
            number of bits for the qiskit_bit_generator (i.e. 32 or 64).

        RETURNS
        -------
        out: str
            Bitstring of lenght `n_bits`.
        """
        return self._qiskit_bit_generator.random_bitstring(n_bits)

    def get_random_complex_polar(self, r: float, theta: float = 2 * math.pi):
        """
        Returns a random complex in rectangular form from a given polar range.
        If no max angle given, [0,2pi) used.

        PARAMETERS
        ----------
        r: float
            Real lower bound for the random number.
        theta: float, default 2pi
            Real strict upper bound for the random number.

        RETURNS
        -------
        out: complex
            Random complex in the range [0,r) * exp{ j[0,theta) }.
        """
        r0: float = r * math.sqrt(self.get_random_float(0, 1))
        theta0: float = self.get_random_float(0, theta)
        return r0 * math.cos(theta0) + r0 * math.sin(theta0) * 1j

    def get_random_complex_rect(
        self,
        r1: float,
        r2: float,
        i1: Optional[float] = None,
        i2: Optional[float] = None,
    ):
        """
        Returns a random complex with both real and imaginary parts from the
        given ranges. If no imaginary range specified, real range used.

        PARAMETERS
        ----------
        r1: float
            Real lower bound for the random number.
        r2: float
            Real strict upper bound for the random number.
        i1: float, default None
            Imaginary lower bound for the random number.
        i2: float, default None
            Imaginary strict upper bound for the random number.

        RETURNS
        -------
        out: complex
            Random complex in the range [r1,r2) + j[i1,i2).
        """
        re: float = self.get_random_float(r1, r2)
        if i1 is None or i2 is None:
            im: float = self.get_random_float(r1, r2)
        else:
            im = self.get_random_float(i1, i2)
        return re + im * 1j

    def get_random_double(self, min: float, max: float):
        """
        Returns a random double from a uniform distribution in the range
        [min,max).

        PARAMETERS
        ----------
        min: float
            Lower bound for the random number.
        max: float
            Strict upper bound for the random number.

        RETURNS
        -------
        out: float
            Random float in the range [min,max).
        """
        delta: float = max - min
        shifted: float = self._qiskit_bit_generator.random_double(delta)
        return shifted + min

    def get_random_float(self, min: float, max: float):
        """
        Returns a random float from a uniform distribution in the range
        [min,max).

        PARAMETERS
        ----------
        min: float
            Lower bound for the random number.
        max: float
            Strict upper bound for the random number.

        RETURNS
        -------
        out: float
            Random float in the range [min,max).
        """
        unpacked = 0x3F800000 | self.get_random_int32() >> 9
        packed = struct.pack("I", unpacked)
        shifted = struct.unpack("f", packed)[0] - 1.0
        return (max - min) * shifted + min

    def get_random_int(self, min: int, max: int):
        """
        Returns a random integer between and including [min, max].

        PARAMETERS
        ----------
        min: int
            Lower bound for the random int.
        max: int
            Upper bound for the random int.

        RETURNS
        -------
        out: int
            Random int in the range [min,max].
        """
        delta: int = max - min
        n_bits: int = math.floor(math.log(delta, 2)) + 1
        shifted: int = self._qiskit_bit_generator.random_uint(n_bits)
        while shifted > delta:
            shifted = self._qiskit_bit_generator.random_uint(n_bits)
        return shifted + min

    def get_random_int32(self):
        """
        Returns a random 32 bit unsigned integer from a uniform distribution.

        RETURNS
        -------
        out: int
            Random 32 bit unsigned int.
        """
        return self._qiskit_bit_generator.random_uint(32)

    def get_random_int64(self):
        """
        Returns a random 32 bit unsigned integer from a uniform distribution.

        RETURNS
        -------
        out: int
            Random 32 bit unsigned int.
        """
        return self._qiskit_bit_generator.random_uint(64)

    ############################ PUBLIC PROPERTIES ############################
    @property
    def state(self) -> dict:
        """
        The state of the Qrng object.
        """
        return {
            "qiskit_bit_generator": self._qiskit_bit_generator.state,
        }
