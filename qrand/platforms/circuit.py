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

from abc import ABC, abstractmethod

from ..helpers import validate_natural


###############################################################################
## QUANTUM CIRCUIT INTERFACE (ADAPTER)
###############################################################################
class QuantumCircuit(ABC):
    @abstractmethod
    def __init__(self, num_qubits: int) -> None:
        pass

    @property
    @abstractmethod
    def num_qubits(self) -> int:
        pass

    ############################## SPECIAL GATES ##############################
    @abstractmethod
    def measure(self, target_qubit: int) -> None:
        pass

    ########################### SINGLE QUBIT GATES ###########################
    @abstractmethod
    def h(self, target_qubit: int) -> None:
        pass

    @abstractmethod
    def rx(self, radians: float, target_qubit: int) -> None:
        pass

    @abstractmethod
    def ry(self, radians: float, target_qubit: int) -> None:
        pass

    @abstractmethod
    def rz(self, radians: float, target_qubit: int) -> None:
        pass

    @abstractmethod
    def s(self, target_qubit: int) -> None:
        pass

    @abstractmethod
    def t(self, target_qubit: int) -> None:
        pass

    @abstractmethod
    def u1(self, theta: float, target_qubit: int) -> None:
        pass

    @abstractmethod
    def u2(self, phi: float, lam: float, target_qubit: int) -> None:
        pass

    @abstractmethod
    def u3(
        self, theta: float, phi: float, lam: float, target_qubit: int
    ) -> None:
        pass

    @abstractmethod
    def x(self, target_qubit: int) -> None:
        pass

    @abstractmethod
    def y(self, target_qubit: int) -> None:
        pass

    @abstractmethod
    def z(self, target_qubit: int) -> None:
        pass

    ############################# TWO QUBIT GATES #############################
    @abstractmethod
    def cs(self, control_qubit: int, target_qubit: int) -> None:
        pass

    @abstractmethod
    def cx(self, control_qubit: int, target_qubit: int) -> None:
        pass

    @abstractmethod
    def cz(self, control_qubit: int, target_qubit: int) -> None:
        pass

    @abstractmethod
    def swap(self, target_qubit_1: int, target_qubit_2: int) -> None:
        pass

    ############################ THREE QUBIT GATES ############################
    @abstractmethod
    def ccx(
        self, control_qubit_1: int, control_qubit_2: int, target_qubit: int
    ) -> None:
        pass

    @abstractmethod
    def cswap(
        self, control_qubit_1: int, control_qubit_2: int, target_qubit: int
    ) -> None:
        pass

    ############################## ALIAS GATES ##############################
    def cnot(self, control_qubit: int, target_qubit: int) -> None:
        self.cx(control_qubit, target_qubit)

    def cphase(self, control_qubit: int, target_qubit: int) -> None:
        self.cs(control_qubit, target_qubit)

    def fredkin(
        self, control_qubit_1: int, control_qubit_2: int, target_qubit: int
    ) -> None:
        self.cswap(control_qubit_1, control_qubit_2, target_qubit)

    def hadamard(self, target_qubit: int) -> None:
        self.h(target_qubit)

    def phase(self, target_qubit: int) -> None:
        self.s(target_qubit)

    def pi8(self, target_qubit: int) -> None:
        self.t(target_qubit)

    def toffoli(
        self, control_qubit_1: int, control_qubit_2: int, target_qubit: int
    ) -> None:
        self.ccx(control_qubit_1, control_qubit_2, target_qubit)

    ############################## PRIVATE API ##############################
    def _validate_qubit_index(self, qubit_index: int) -> None:
        validate_natural(qubit_index, zero=True)
        if qubit_index >= self.num_qubits:
            raise ValueError(
                f"Qubit index out of range {qubit_index} >= {self.num_qubits}."
            )
