##    _____  _____
##   |  __ \|  __ \    AUTHOR: Vishnu Ajith, Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: May 31, 2021
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

from math import erfc, sqrt

from ..helpers import ALPHABETS, validate_numeral
from . import ValidationStrategy


class MonobitFrequencyValidation(ValidationStrategy):
    """
    Frequency (Monobit) Test: pg. 2-2 in [1]_.

    The focus of the test is the proportion of zeroes and ones for the entire
    sequence. The purpose of this test is to determine whether the number of
    ones and zeros in a sequence are approximately the same as would be
    expected for a truly random sequence. The test assesses the closeness of
    the fraction of ones to 1/2, that is, the number of ones and zeroes in a
    sequence should be about the same.

    Methods
    -------
    validate(bitstring: str) -> bool
        Validates the randomness/entropy in an input bitstring.

    Notes
    -----
    It is recommended that each sequence to be tested consist of a minimum of
    100 bits (i.e., n ≥ 100). All subsequent tests in [1]_ depend on the
    passing of this test.

    References
    ----------
    .. [1] Lawrence Bassham, Andrew Rukhin, Juan Soto, James Nechvatal, Miles
        Smid, Elaine Barker, Stefan Leigh, Mark Levenson, Mark Vangel, David
        Banks, N. Heckert, James Dray (2010) A Statistical Test Suite for
        Random and Pseudorandom Number Generators for Cryptographic
        Applications. (U.S. Department of Commerce, Washington, D.C.), Special
        Publication (SP) 800-22, Rev. 1a, Final April 30, 2010.
        https://doi.org/10.6028/NIST.SP.800-22r1a
    """

    def validate(self, bitstring: str) -> bool:
        validate_numeral(bitstring, ALPHABETS["BINARY"])
        n = len(bitstring)
        if n < 100:
            return False
        s_n = 0.0
        for bit in bitstring:
            s_n += 2 * int(bit) - 1
        s_obs = s_n / sqrt(n)
        p_value = erfc(s_obs / sqrt(2))
        return p_value >= 0.01
