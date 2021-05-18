##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: May 18, 2021
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

from ..circuit import QuantumCircuit


###############################################################################
## CIRQ CIRCUIT
###############################################################################
class CirqCircuit(QuantumCircuit):
    def __init__(self, num_qubits: int) -> None:
        self.ERROR_MSG = f"{self.__class__.__name__}"  # TODO
        raise NotImplementedError(self.ERROR_MSG)

    @property
    def num_qubits(self) -> int:
        raise NotImplementedError(self.ERROR_MSG)

    ############################## SPECIAL GATES ##############################
    def measure(self, target_qubit: int) -> None:
        raise NotImplementedError(self.ERROR_MSG)

    ########################### SINGLE QUBIT GATES ###########################
    def h(self, target_qubit: int) -> None:
        raise NotImplementedError(self.ERROR_MSG)

    def rx(self, radians: float, target_qubit: int) -> None:
        raise NotImplementedError(self.ERROR_MSG)

    def ry(self, radians: float, target_qubit: int) -> None:
        raise NotImplementedError(self.ERROR_MSG)

    def rz(self, radians: float, target_qubit: int) -> None:
        raise NotImplementedError(self.ERROR_MSG)

    def s(self, target_qubit: int) -> None:
        raise NotImplementedError(self.ERROR_MSG)

    def t(self, target_qubit: int) -> None:
        raise NotImplementedError(self.ERROR_MSG)

    def u1(self, theta: float, target_qubit: int) -> None:
        raise NotImplementedError(self.ERROR_MSG)

    def u2(self, phi: float, lam: float, target_qubit: int) -> None:
        raise NotImplementedError(self.ERROR_MSG)

    def u3(
        self, theta: float, phi: float, lam: float, target_qubit: int
    ) -> None:
        raise NotImplementedError(self.ERROR_MSG)

    def x(self, target_qubit: int) -> None:
        raise NotImplementedError(self.ERROR_MSG)

    def y(self, target_qubit: int) -> None:
        raise NotImplementedError(self.ERROR_MSG)

    def z(self, target_qubit: int) -> None:
        raise NotImplementedError(self.ERROR_MSG)

    ############################# TWO QUBIT GATES #############################
    def cs(self, control_qubit: int, target_qubit: int) -> None:
        raise NotImplementedError(self.ERROR_MSG)

    def cx(self, control_qubit: int, target_qubit: int) -> None:
        raise NotImplementedError(self.ERROR_MSG)

    def cz(self, control_qubit: int, target_qubit: int) -> None:
        raise NotImplementedError(self.ERROR_MSG)

    def swap(self, target_qubit_1: int, target_qubit_2: int) -> None:
        raise NotImplementedError(self.ERROR_MSG)

    ############################ THREE QUBIT GATES ############################
    def ccx(
        self, control_qubit_1: int, control_qubit_2: int, target_qubit: int
    ) -> None:
        raise NotImplementedError(self.ERROR_MSG)

    def cswap(
        self, control_qubit_1: int, control_qubit_2: int, target_qubit: int
    ) -> None:
        raise NotImplementedError(self.ERROR_MSG)
