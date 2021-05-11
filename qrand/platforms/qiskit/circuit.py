##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: April 20, 2021
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

from qiskit import QuantumCircuit as QiskitQuantumCircuit

from ..circuit import QuantumCircuit


###############################################################################
## QISKIT CIRCUIT
###############################################################################
class QiskitCircuit(QuantumCircuit, QiskitQuantumCircuit):
    def __init__(self, num_qubits: int) -> None:
        super(QuantumCircuit, self).__init__(num_qubits, num_qubits)

    ############################### PUBLIC API ###############################
    @property
    def num_qubits(self) -> int:
        return super(QuantumCircuit, self).num_qubits

    def h(self, target_qubit: int) -> None:
        super(QuantumCircuit, self).h(target_qubit)

    def cx(self, control_qubit: int, target_qubit: int) -> None:
        super(QuantumCircuit, self).cx(control_qubit, target_qubit)

    def measure(self, target_qubit: int) -> None:
        super(QuantumCircuit, self).measure(target_qubit, target_qubit)
