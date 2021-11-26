##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: November 25, 2021
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

from typing import cast

from qiskit import QuantumCircuit as QiskitQuantumCircuit

from ..circuit import QuantumCircuit


###############################################################################
## QISKIT CIRCUIT
###############################################################################
class QiskitCircuit(QiskitQuantumCircuit, QuantumCircuit):
    def __init__(self, num_qubits: int) -> None:
        super().__init__(num_qubits, num_qubits)  # type: ignore

    @property
    def num_qubits(self) -> int:
        return cast(int, super().num_qubits)

    ############################## SPECIAL GATES ##############################
    def measure(self, target_qubit: int) -> None:
        super().measure(target_qubit, target_qubit)  # type: ignore

    ########################### SINGLE QUBIT GATES ###########################
    def h(self, target_qubit: int) -> None:
        super().h(target_qubit)

    def rx(self, radians: float, target_qubit: int) -> None:
        super().rx(radians, target_qubit)

    def ry(self, radians: float, target_qubit: int) -> None:
        super().ry(radians, target_qubit)

    def rz(self, radians: float, target_qubit: int) -> None:
        super().rz(radians, target_qubit)

    def s(self, target_qubit: int) -> None:
        super().s(target_qubit)

    def t(self, target_qubit: int) -> None:
        super().t(target_qubit)

    def u1(self, theta: float, target_qubit: int) -> None:
        super().u1(theta, target_qubit)

    def u2(self, phi: float, lam: float, target_qubit: int) -> None:
        super().u2(phi, lam, target_qubit)

    def u3(
        self, theta: float, phi: float, lam: float, target_qubit: int
    ) -> None:
        super().u3(theta, phi, lam, target_qubit)

    def x(self, target_qubit: int) -> None:
        super().x(target_qubit)

    def y(self, target_qubit: int) -> None:
        super().y(target_qubit)

    def z(self, target_qubit: int) -> None:
        super().z(target_qubit)

    ############################# TWO QUBIT GATES #############################
    def cs(self, control_qubit: int, target_qubit: int) -> None:
        super().cs(control_qubit, target_qubit)

    def cx(self, control_qubit: int, target_qubit: int) -> None:
        super().cx(control_qubit, target_qubit)

    def cz(self, control_qubit: int, target_qubit: int) -> None:
        super().cz(control_qubit, target_qubit)

    def swap(self, target_qubit_1: int, target_qubit_2: int) -> None:
        super().swap(target_qubit_1, target_qubit_2)

    ############################ THREE QUBIT GATES ############################
    def ccx(
        self, control_qubit_1: int, control_qubit_2: int, target_qubit: int
    ) -> None:
        super().ccx(control_qubit_1, control_qubit_2, target_qubit)

    def cswap(
        self, control_qubit: int, target_qubit_1: int, target_qubit_2: int
    ) -> None:
        super().cswap(control_qubit, target_qubit_1, target_qubit_2)
