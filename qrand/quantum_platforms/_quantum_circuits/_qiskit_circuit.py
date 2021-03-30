##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: March 27, 2021
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

from . import QuantumCircuit


###############################################################################
## QISKIT CIRCUIT
###############################################################################
class QiskitCircuit(QuantumCircuit):
    def __init__(self, num_qubits: int) -> None:
        self._base_circuit = QiskitQuantumCircuit(num_qubits, num_qubits)

    @property
    def num_qubits(self) -> int:
        return self._base_circuit.num_qubits

    def h(self, target_qubit: int) -> None:
        self._base_circuit.h(target_qubit)

    def cx(self, control_qubit: int, target_qubit: int) -> None:
        self._base_circuit.cx(control_qubit, target_qubit)

    def measure(self, target_qubit: int) -> None:
        self._base_circuit.measure(target_qubit, target_qubit)

    def extract_base_circuit(self) -> QiskitQuantumCircuit:
        return self._base_circuit
