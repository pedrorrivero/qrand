##    _____  _____
##   |  __ \|  __ \    AUTHOR: Vishnu Ajith, Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: June 1, 2021
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


class RunsValidation(ValidationStrategy):
    """
    Runs Test: pg. 2-5 in [1]_.

    The focus of this test is the total number of runs in the sequence, where a
    run is an uninterrupted sequence of identical bits. A run of length k
    consists of exactly k identical bits and is bounded before and after with a
    bit of the opposite value. The purpose of the runs test is to determine
    whether the number of runs of ones and zeros of various lengths is as
    expected for a random sequence. In particular, this test determines whether
    the oscillation between such zeros and ones is too fast or too slow.

    Methods
    -------
    validate(bitstring:str) -> bool
        Validates the randomness/entropy in an input bitstring.

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
        pi = bitstring.count("1") / n
        # validating whether frequency run test was run
        if abs(pi - 1) >= 2 / sqrt(n):
            return False
        v_obs = 1
        for i in range(0, n - 1):
            if bitstring[i] != bitstring[i + 1]:
                v_obs += 1
        p_value = erfc(
            (v_obs - (2 * n * pi * (1 - pi)))
            / (2 * sqrt(2 * n) * pi * (1 - pi))
        )
        return p_value >= 0.01
