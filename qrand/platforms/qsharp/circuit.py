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
## QSHARP CIRCUIT
###############################################################################
class QsharpCircuit(QuantumCircuit):
    def __init__(self, num_qubits: int) -> None:
        self.gates: str = ""
        self._num_qubits: int = num_qubits
        self.ERROR_MSG = f"{self.__class__.__name__}"  # TODO

    def _validate_qubit_index(self, qubit_index: int) -> None:
        if qubit_index >= self.num_qubits:
            raise ValueError(
                f"Qubit index out of range {qubit_index} >= {self.num_qubits}."
            )

    @property
    def num_qubits(self) -> int:
        return self._num_qubits

    ############################## SPECIAL GATES ##############################
    def measure(self, target_qubit: int) -> None:
        self._validate_qubit_index(target_qubit)
        self.gates += f"""
        if M(q[{target_qubit}]) == One{{
        set value w/= {target_qubit} <- "1";
        }}
        """

    ########################### SINGLE QUBIT GATES ###########################
    def h(self, target_qubit: int) -> None:
        self._validate_qubit_index(target_qubit)
        self.gates += f"H(q[{target_qubit}]);"

    def rx(self, radians: float, target_qubit: int) -> None:
        self._validate_qubit_index(target_qubit)
        self.gates += f"Rx({radians},q[{target_qubit}]);"

    def ry(self, radians: float, target_qubit: int) -> None:
        self._validate_qubit_index(target_qubit)
        self.gates += f"Ry({radians},q[{target_qubit}]);"

    def rz(self, radians: float, target_qubit: int) -> None:
        self._validate_qubit_index(target_qubit)
        self.gates += f"Rz({radians},q[{target_qubit}]);"

    def s(self, target_qubit: int) -> None:
        self._validate_qubit_index(target_qubit)
        self.gates += f"S(q[{target_qubit}]);"

    def t(self, target_qubit: int) -> None:
        self._validate_qubit_index(target_qubit)
        self.gates += f"T(q[{target_qubit}]);"

    def u1(self, theta: float, target_qubit: int) -> None:
        self._validate_qubit_index(target_qubit)
        self.gates += f"R1({theta},q[{target_qubit}]);"

    def u2(self, phi: float, lam: float, target_qubit: int) -> None:
        raise NotImplementedError(self.ERROR_MSG)

    def u3(
        self, theta: float, phi: float, lam: float, target_qubit: int
    ) -> None:
        raise NotImplementedError(self.ERROR_MSG)

    def x(self, target_qubit: int) -> None:
        self._validate_qubit_index(target_qubit)
        self.gates += f"X(q[{target_qubit}]);"

    def y(self, target_qubit: int) -> None:
        self._validate_qubit_index(target_qubit)
        self.gates += f"Y(q[{target_qubit}]);"

    def z(self, target_qubit: int) -> None:
        self._validate_qubit_index(target_qubit)
        self.gates += f"Z(q[{target_qubit}]);"

    ############################# TWO QUBIT GATES #############################
    def cs(self, control_qubit: int, target_qubit: int) -> None:
        self._validate_qubit_index(control_qubit)
        self._validate_qubit_index(target_qubit)
        self.gates += f"""
        Controlled S(q[{control_qubit}],q[{target_qubit}]);
        """

    def cx(self, control_qubit: int, target_qubit: int) -> None:
        self._validate_qubit_index(control_qubit)
        self._validate_qubit_index(target_qubit)
        self.gates += f"CNOT(q[{control_qubit}],q[{target_qubit}]);"

    def cz(self, control_qubit: int, target_qubit: int) -> None:
        self._validate_qubit_index(control_qubit)
        self._validate_qubit_index(target_qubit)
        self.gates += f"CZ(q[{control_qubit}],q[{target_qubit}]);"

    def swap(self, target_qubit_1: int, target_qubit_2: int) -> None:
        self._validate_qubit_index(target_qubit_1)
        self._validate_qubit_index(target_qubit_2)
        self.gates += f"SWAP(q[{target_qubit_1}],q[{target_qubit_2}]);"

    ############################ THREE QUBIT GATES ############################
    def ccx(
        self, control_qubit_1: int, control_qubit_2: int, target_qubit: int
    ) -> None:
        self._validate_qubit_index(control_qubit_1)
        self._validate_qubit_index(control_qubit_2)
        self._validate_qubit_index(target_qubit)
        self.gates += f"""
        CCNOT(q[{control_qubit_1}],q[{control_qubit_2}],q[{target_qubit}]);
        """

    def cswap(
        self, control_qubit_1: int, control_qubit_2: int, target_qubit: int
    ) -> None:
        self._validate_qubit_index(control_qubit_1)
        self._validate_qubit_index(control_qubit_2)
        self._validate_qubit_index(target_qubit)
        self.gates += f"""
        CSWAP(q[{control_qubit_1},q[{control_qubit_2}],q[{target_qubit}]);
        """
