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

from typing import cast

from qiskit import QuantumCircuit as QiskitQuantumCircuit

from ..circuit import QuantumCircuit


###############################################################################
## QISKIT CIRCUIT
###############################################################################
class QiskitCircuit(QuantumCircuit, QiskitQuantumCircuit):
    def __init__(self, num_qubits: int) -> None:
        super(QuantumCircuit, self).__init__(num_qubits, num_qubits)

    @property
    def num_qubits(self) -> int:
        return cast(int, super(QuantumCircuit, self).num_qubits)

    ############################## SPECIAL GATES ##############################
    def measure(self, target_qubit: int) -> None:
        super(QuantumCircuit, self).measure(target_qubit, target_qubit)

    ########################### SINGLE QUBIT GATES ###########################
    def h(self, target_qubit: int) -> None:
        super(QuantumCircuit, self).h(target_qubit)

    def rx(self, radians: float, target_qubit: int) -> None:
        super(QuantumCircuit, self).rx(radians, target_qubit)

    def ry(self, radians: float, target_qubit: int) -> None:
        super(QuantumCircuit, self).ry(radians, target_qubit)

    def rz(self, radians: float, target_qubit: int) -> None:
        super(QuantumCircuit, self).rz(radians, target_qubit)

    def s(self, target_qubit: int) -> None:
        super(QuantumCircuit, self).s(target_qubit)

    def t(self, target_qubit: int) -> None:
        super(QuantumCircuit, self).t(target_qubit)

    def u1(self, theta: float, target_qubit: int) -> None:
        super(QuantumCircuit, self).u1(theta, target_qubit)

    def u2(self, phi: float, lam: float, target_qubit: int) -> None:
        super(QuantumCircuit, self).u2(phi, lam, target_qubit)

    def u3(
        self, theta: float, phi: float, lam: float, target_qubit: int
    ) -> None:
        super(QuantumCircuit, self).u3(theta, phi, lam, target_qubit)

    def x(self, target_qubit: int) -> None:
        super(QuantumCircuit, self).x(target_qubit)

    def y(self, target_qubit: int) -> None:
        super(QuantumCircuit, self).y(target_qubit)

    def z(self, target_qubit: int) -> None:
        super(QuantumCircuit, self).z(target_qubit)

    ############################# TWO QUBIT GATES #############################
    def cs(self, control_qubit: int, target_qubit: int) -> None:
        super(QuantumCircuit, self).cs(control_qubit, target_qubit)

    def cx(self, control_qubit: int, target_qubit: int) -> None:
        super(QuantumCircuit, self).cx(control_qubit, target_qubit)

    def cz(self, control_qubit: int, target_qubit: int) -> None:
        super(QuantumCircuit, self).cz(control_qubit, target_qubit)

    def swap(self, target_qubit_1: int, target_qubit_2: int) -> None:
        super(QuantumCircuit, self).swap(target_qubit_1, target_qubit_2)

    ############################ THREE QUBIT GATES ############################
    def ccx(
        self, control_qubit_1: int, control_qubit_2: int, target_qubit: int
    ) -> None:
        super(QuantumCircuit, self).ccx(
            control_qubit_1, control_qubit_2, target_qubit
        )

    def cswap(
        self, control_qubit: int, target_qubit_1: int, target_qubit_2: int
    ) -> None:
        super(QuantumCircuit, self).cswap(
            control_qubit, target_qubit_1, target_qubit_2
        )
