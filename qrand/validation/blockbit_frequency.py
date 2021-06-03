##    _____  _____
##   |  __ \|  __ \    AUTHOR: Vishnu Ajith, Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: June 3, 2021
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

from math import floor

from scipy.special import gammaincc

from ..helpers import ALPHABETS, validate_natural_number, validate_numeral
from . import ValidationStrategy


class BlockFrequencyValidation(ValidationStrategy):
    """
    Frequency Test within a Block: pg. 2-4 in [1]_.

    The focus of the test is the proportion of ones within M-bit blocks. The
    purpose of this test is to determine whether the frequency of ones in an
    M-bit block is approximately M/2, as would be expected under an assumption
    of randomness.

    Parameters
    ----------
    blocksize: int, default: 1
        The length M of each block in the test.

    Attributes
    ----------
    blocksize: int
        The length M of each block in the test.

    Methods
    -------
    validate(bitstring: str) -> bool
        Validates the randomness/entropy in an input bitstring.

    Notes
    -----
    It is recommended that each sequence to be tested consist of a minimum of
    100 bits (i.e., n >= 100). Note that n >= MN. The block size M should be
    selected such that M >= 20, M > 0.01n and N < 100. For block size M=1, this
    test degenerates to the Frequency (Monobit) test.

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

    ################################ SPECIFICS ################################
    def __init__(self, blocksize: int = 1) -> None:
        self.blocksize = blocksize

    @property
    def blocksize(self) -> int:
        """
        The length M of each block in the test.
        """
        return self._blocksize

    @blocksize.setter
    def blocksize(self, blocksize: int):
        validate_natural_number(blocksize, zero=False)
        self._blocksize: int = blocksize

    ############################### VALIDATION ###############################
    def validate(self, bitstring: str) -> bool:
        validate_numeral(bitstring, ALPHABETS["BINARY"])
        n = len(bitstring)
        if n < 100:
            return False
        N = floor(n / self.blocksize)
        ki_square_obs = 0.0
        for i in range(N):
            block = bitstring[i * self.blocksize : (i + 1) * self.blocksize]
            pi = block.count("1") / self.blocksize
            ki_square_obs += (pi - 0.5) ** 2
        ki_square_obs *= 4 * self.blocksize
        p_value = gammaincc(N / 2, ki_square_obs / 2)
        return p_value >= 0.01
