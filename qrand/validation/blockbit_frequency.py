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

from math import floor

from scipy.special import gammaincc

from . import ValidationStrategy


class BlockbitFrequencyValidation:
    """
    Frequency (Monobit) Test: pg. 2-2 in [1]_.

    Methods
    -------
    __init__(blocksize:int)
        initializes classes instance with blocksize for the testing

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

    def __init__(self, blocksize: int) -> None:
        super().__init__()
        self.blocksize = blocksize

    def validate(self, bitstring: str) -> bool:
        n = len(bitstring)
        # calculating number of blocks
        N = floor(n / self.blocksize)
        ki_square_obs = 0.0
        for i in range(N):
            pi = (
                bitstring[i * self.blocksize : (i + 1) * self.blocksize].count(
                    "1"
                )
                / self.blocksize
            )
            ki_square_obs += (pi - 0.5) ** 2
        ki_square_obs *= 4 * self.blocksize
        p_value = gammaincc(self.blocksize / 2, ki_square_obs / 2)
        return p_value > 0.01
