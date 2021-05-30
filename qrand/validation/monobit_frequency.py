##    _____  _____
##   |  __ \|  __ \    AUTHOR: Vishnu Ajith, Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: May 30, 2021
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

from . import ValidationStrategy


class MonobitFrequencyValidation(ValidationStrategy):
    """
    Frequency (Monobit) Test: pg. 2-2 in [1]_.

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
        n = len(bitstring)
        s_n = 0.0
        for bit in bitstring:
            s_n += 2 * int(bit) - 1
        s_obs = s_n / sqrt(n)
        p_value = erfc(s_obs / sqrt(2))
        return p_value >= 0.01
