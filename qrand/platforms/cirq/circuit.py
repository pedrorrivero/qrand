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
import cirq
from cirq.circuits import Circuit as CirqQuantumCircuit
from ..circuit import QuantumCircuit
from ...helpers import validate_natural_number, validate_type

###############################################################################
## CIRQ CIRCUIT
###############################################################################
class CirqCircuit(QuantumCircuit):
   
    def __init__(self, num_qubits: int) -> None:
        self.qubits=cirq.LineQubit.range(num_qubits)
        self._num_qubits=num_qubits
        self.moment_list:list=[]
    
    def _validate_qubit_index(self, qubit_index: int) -> None:
        if qubit_index >= self.num_qubits:
            raise ValueError(
                f"Qubit index out of range {qubit_index} >= {self.num_qubits}."
            )

    
    
    @property
    def num_qubits(self) -> int:
        return self._num_qubits

    @num_qubits.setter
    def num_qubits(self,num_qubits:int) -> None:
        self._num_qubits=num_qubits

    ############################## SPECIAL GATES ##############################
    def measure(self, target_qubit: int) -> None:
        self.moment_list.append(cirq.ops.measure(self.qubits[target_qubit]))
        
    ########################### SINGLE QUBIT GATES ###########################
    def h(self, target_qubit: int) -> None:
        validate_natural_number(target_qubit, True)
        self._validate_qubit_index(target_qubit)
        self.moment_list.append(cirq.ops.H(self.qubits[target_qubit]))


    def rx(self, radians: float, target_qubit: int) -> None:
        validate_natural_number(target_qubit, True)
        self._validate_qubit_index(target_qubit)
        self.moment_list.append(cirq.ops.Rx(radians, self.qubits[target_qubit]))

    def ry(self, radians: float, target_qubit: int) -> None:
        validate_natural_number(target_qubit, True)
        self._validate_qubit_index(target_qubit)
        self.moment_list.append(cirq.ops.Ry(radians,self.qubits[target_qubit]))

    def rz(self, radians: float, target_qubit: int) -> None:
        validate_natural_number(target_qubit, True)
        self._validate_qubit_index(target_qubit)
        self.moment_list.append(cirq.ops.Rz(radians, self.qubits[target_qubit]))

    def s(self, target_qubit: int) -> None:
        validate_natural_number(target_qubit, True)
        self._validate_qubit_index(target_qubit)
        self.moment_list.append(cirq.ops.S(self.qubits[target_qubit]))

    def t(self, target_qubit: int) -> None:
        validate_natural_number(target_qubit, True)
        self._validate_qubit_index(target_qubit)
        self.moment_list.append(cirq.ops.T(self.qubits[target_qubit]))

    def x(self, target_qubit: int) -> None:
        validate_natural_number(target_qubit, True)
        self._validate_qubit_index(target_qubit)
        self.moment_list.append(cirq.ops.X(self.qubits[target_qubit]))


    def y(self, target_qubit: int) -> None:
        validate_natural_number(target_qubit, True)
        self._validate_qubit_index(target_qubit)
        self.moment_list.append(cirq.ops.Y(self.qubits[target_qubit]))


    def z(self, target_qubit: int) -> None:
        validate_natural_number(target_qubit, True)
        self._validate_qubit_index(target_qubit)
        self.moment_list.append(cirq.ops.Z(self.qubits[target_qubit]))

    ############################# TWO QUBIT GATES #############################
    def cz(self, control_qubit: int, target_qubit: int) -> None:
        validate_natural_number(target_qubit, True)
        validate_natural_number(control_qubit, True)
        self._validate_qubit_index(target_qubit)
        self._validate_qubit_index(control_qubit)
        self.moment_list.append(cirq.ops.CZ(self.qubits[control_qubit], self.qubits[target_qubit]))

    def swap(self, target_qubit_1: int, target_qubit_2: int) -> None:
        validate_natural_number(target_qubit_1, True)
        self._validate_qubit_index(target_qubit_1)
        self._validate_qubit_index(target_qubit_2)
        self.moment_list.append(cirq.ops.SWAP(self.qubits[target_qubit_1], self.qubits[target_qubit_2]))

    ############################ THREE QUBIT GATES ############################


    def cswap(
        self, control_qubit: int, target_qubit_1: int, target_qubit_2: int
    ) -> None:
        validate_natural_number(target_qubit_1, True)
        validate_natural_number(target_qubit_2, True)
        validate_natural_number(control_qubit, True)
        self._validate_qubit_index(control_qubit)
        self._validate_qubit_index(target_qubit_1)
        self._validate_qubit_index(target_qubit_2)
        self.moment_list.append(cirq.ops.CSWAP(self.qubits[control_qubit], self.qubits[target_qubit_1], self.qubits[target_qubit_2]))

    def createcircuit(self):
        return CirqQuantumCircuit(self.moment_list)