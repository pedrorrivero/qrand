##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: May 20, 2021
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

from abc import abstractmethod

from ..protocols import QuantumProtocol
from .factory import QuantumFactory


###############################################################################
## QUANTUM PLATFORM INTERFACE (CLASS DECORATOR)
###############################################################################
class QuantumPlatform(QuantumFactory):
    """
    A class decorator for QuantumFactory which adds functionality to fetch
    random bits following a given protocol.

    Parameters
    ----------
    Same as QuantumFactory.

    Attributes
    ----------
    Same as QuantumFactory.

    Methods
    -------
    Same as QuantumFactory.
    fetch_random_bits(protocol: QuantumProtocol) -> str:
        Retrieves a string of random bits following a given protocol.
    """

    @abstractmethod
    def fetch_random_bits(self, protocol: QuantumProtocol) -> str:
        """
        Retrieves a string of random bits following a given protocol.

        Parameters
        ----------
        protocol: QuantumProtocol
            The protocol to generate random bits.

        Returns
        -------
        out: str
            A string of random bits.
        """
        pass
