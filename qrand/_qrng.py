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

from ._qiskit_bitgenerator import QiskitBitGenerator


###############################################################################
## QRNG
###############################################################################
class Qrng:
    """
    COPYRIGHT NOTICE
    ----------------
    Source: https://github.com/ozanerhansha/qRNG
    License: GNU GENERAL PUBLIC LICENSE VERSION 3
    Changes:
        - Substituted random generation and caching logic
    """

    def __init__(self, quantum_bit_generator):
        self.quantum_bit_generator = quantum_bit_generator

    # Returns a random n-bit string by popping n bits from bitCache.
    def get_bit_string(self, n_bits):
        """
        Returns a random bitstring of a given lenght.

        ARGUMENTS
        ---------
        n_bits: int
            Number of bits to retrieve. If less than one it defaults to the raw
            number of bits for the quantum_bit_generator (i.e. 32 or 64).

        RETURNS
        -------
        out: str
            Bitstring of lenght `n_bits`.
        """
        return self.quantum_bit_generator.random_bitstring(n_bits)

    # Returns a random integer between and including [min, max].
    # Running time is probabalistic but complexity is still O(n)
    def get_random_int(self, min, max):
        delta = max - min
        n = math.floor(math.log(delta, 2)) + 1
        result = int(self.get_bit_string(n), 2)
        while result > delta:
            result = int(self.get_bit_string(n), 2)
        return result + min

    def get_random_int32(self):
        """
        Returns a random 32 bit unsigned integer from a uniform distribution.

        RETURNS
        -------
        out: int
            Random 32 bit unsigned int.
        """
        return self.quantum_bit_generator.random_uint(32)

    def get_random_int64(self):
        """
        Returns a random 32 bit unsigned integer from a uniform distribution.

        RETURNS
        -------
        out: int
            Random 32 bit unsigned int.
        """
        return self.quantum_bit_generator.random_uint(64)

    # Returns a random float from a uniform distribution in the range [min, max).
    def get_random_float(self, min, max):
        # Get random float from [0,1)
        unpacked = 0x3F800000 | self.get_random_int32() >> 9
        packed = struct.pack("I", unpacked)
        value = struct.unpack("f", packed)[0] - 1.0
        return (max - min) * value + min

    def get_random_double(self, min, max):
        """
        Returns a random double from a uniform distribution in the range
        [min,max).

        ARGUMENTS
        ---------
        min: float
            Lower bound for the random number.
        max: float
            Strict upper bound for the random number.

        RETURNS
        -------
        out: float
            Random float in the range [min,max).
        """
        range = max - min
        value = self.quantum_bit_generator.random_double(range)
        return value + min

    # Returns a random complex with both real and imaginary parts
    # from the given ranges. If no imaginary range specified, real range used.
    def get_random_complex_rect(self, r1, r2, i1=None, i2=None):
        re = self.get_random_float(r1, r2)
        if i1 is None or i2 is None:
            im = self.get_random_float(r1, r2)
        else:
            im = self.get_random_float(i1, i2)
        return re + im * 1j

    # Returns a random complex in rectangular form from a given polar range.
    # If no max angle given, [0,2pi) used.
    def get_random_complex_polar(self, r, theta=2 * math.pi):
        r0 = r * math.sqrt(self.get_random_float(0, 1))
        theta0 = self.get_random_float(0, theta)
        return r0 * math.cos(theta0) + r0 * math.sin(theta0) * 1j
