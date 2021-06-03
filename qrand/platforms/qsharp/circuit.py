##    _____  _____
##   |  __ \|  __ \    AUTHOR: A. Nair, P. Rivero
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

from typing import Optional

try:
    from qsharp import QSharpCallable, compile
except ImportError:
    _IMPORT_QSHARP = False
else:
    _IMPORT_QSHARP = (
        True & _IMPORT_QSHARP if "_IMPORT_QSHARP" in globals() else True
    )

from ...helpers import validate_type
from ..circuit import QuantumCircuit


###############################################################################
## QSHARP CIRCUIT
###############################################################################
class QsharpCircuit(QuantumCircuit):
    def __init__(self, num_qubits: int) -> None:
        validate_type(num_qubits, int)
        self._num_qubits: int = num_qubits
        self._gates: str = ""

    @property
    def num_qubits(self) -> int:
        return self._num_qubits

    @property
    def _gates(self) -> str:
        return self.__gates

    @_gates.setter
    def _gates(self, gates: str) -> None:
        validate_type(gates, str)
        self.__gates: str = gates

    def generate_code(self, num_measurements: int = 1) -> QSharpCallable:
        validate_type(num_measurements, int)
        qsharp_code: str = """
        open Microsoft.Quantum.Intrinsic;
        open Microsoft.Quantum.Measurement;
        open Microsoft.Quantum.Arrays;
        open Microsoft.Quantum.Math;

        operation Program():String[]{{

        use q = Qubit[{num_qubits}];
        mutable value = ConstantArray({num_measurements},"");
        mutable res = "";

        for i in IndexRange(value)
        {{
            {gates}
            set value w/= i <- res;
            set res = "";
        }}

        ResetAll(q);
        return value;
        }}
        """
        return compile(
            qsharp_code.format(
                num_qubits=self.num_qubits,
                num_measurements=num_measurements,
                gates=self._gates,
            )
        )

    ############################## SPECIAL GATES ##############################
    def measure(self, target_qubit: int) -> None:
        self._validate_qubit_index(target_qubit)
        self._gates += f"""
        if M(q[{target_qubit}]) == One
        {{
            set res = res+"1";
        }}
        else
        {{
            set res = res+"0";
        }}
        """

    ########################### SINGLE QUBIT GATES ###########################
    def h(self, target_qubit: int) -> None:
        self._validate_qubit_index(target_qubit)
        self._gates += f"H(q[{target_qubit}]);"

    def rx(self, radians: float, target_qubit: int) -> None:
        validate_type(radians, (int, float))
        radians = float(radians)
        self._validate_qubit_index(target_qubit)
        self._gates += f"Rx({radians},q[{target_qubit}]);"

    def ry(self, radians: float, target_qubit: int) -> None:
        validate_type(radians, (int, float))
        radians = float(radians)
        self._validate_qubit_index(target_qubit)
        self._gates += f"Ry({radians},q[{target_qubit}]);"

    def rz(self, radians: float, target_qubit: int) -> None:
        validate_type(radians, (int, float))
        radians = float(radians)
        self._validate_qubit_index(target_qubit)
        self._gates += f"Rz({radians},q[{target_qubit}]);"

    def s(self, target_qubit: int) -> None:
        self._validate_qubit_index(target_qubit)
        self._gates += f"S(q[{target_qubit}]);"

    def t(self, target_qubit: int) -> None:
        self._validate_qubit_index(target_qubit)
        self._gates += f"T(q[{target_qubit}]);"

    def u1(self, theta: float, target_qubit: int) -> None:
        validate_type(theta, (int, float))
        self._validate_qubit_index(target_qubit)
        self._gates += f"R1({float(theta)},q[{target_qubit}]);"

    def u2(self, phi: float, lam: float, target_qubit: int) -> None:
        validate_type(phi, (int, float))
        validate_type(lam, (int, float))
        self._validate_qubit_index(target_qubit)
        self._gates += f"""
        Rz({float(lam)},q[{target_qubit}]);
        Ry(0.5*PI(),q[{target_qubit}]);
        Rz({float(phi)},q[{target_qubit}]);
        """

    def u3(
        self, theta: float, phi: float, lam: float, target_qubit: int
    ) -> None:
        validate_type(theta, (int, float))
        validate_type(phi, (int, float))
        validate_type(lam, (int, float))
        self._validate_qubit_index(target_qubit)
        self._gates += f"""
        Rz({float(lam)},q[{target_qubit}]);
        Rx(0.5*PI(),q[{target_qubit}]);
        Rz({float(theta)},q[{target_qubit}]);
        Rx(-0.5*PI(),q[{target_qubit}]);
        Rz({float(phi)},q[{target_qubit}]);
        """

    def x(self, target_qubit: int) -> None:
        self._validate_qubit_index(target_qubit)
        self._gates += f"X(q[{target_qubit}]);"

    def y(self, target_qubit: int) -> None:
        self._validate_qubit_index(target_qubit)
        self._gates += f"Y(q[{target_qubit}]);"

    def z(self, target_qubit: int) -> None:
        self._validate_qubit_index(target_qubit)
        self._gates += f"Z(q[{target_qubit}]);"

    ############################# TWO QUBIT GATES #############################
    def cs(self, control_qubit: int, target_qubit: int) -> None:
        self._validate_qubit_index(control_qubit)
        self._validate_qubit_index(target_qubit)
        self._gates += f"""
        Controlled S(q[{control_qubit}],q[{target_qubit}]);
        """

    def cx(self, control_qubit: int, target_qubit: int) -> None:
        self._validate_qubit_index(control_qubit)
        self._validate_qubit_index(target_qubit)
        self._gates += f"CNOT(q[{control_qubit}],q[{target_qubit}]);"

    def cz(self, control_qubit: int, target_qubit: int) -> None:
        self._validate_qubit_index(control_qubit)
        self._validate_qubit_index(target_qubit)
        self._gates += f"CZ(q[{control_qubit}],q[{target_qubit}]);"

    def swap(self, target_qubit_1: int, target_qubit_2: int) -> None:
        self._validate_qubit_index(target_qubit_1)
        self._validate_qubit_index(target_qubit_2)
        self._gates += f"SWAP(q[{target_qubit_1}],q[{target_qubit_2}]);"

    ############################ THREE QUBIT GATES ############################
    def ccx(
        self, control_qubit_1: int, control_qubit_2: int, target_qubit: int
    ) -> None:
        self._validate_qubit_index(control_qubit_1)
        self._validate_qubit_index(control_qubit_2)
        self._validate_qubit_index(target_qubit)
        self._gates += f"""
        CCNOT(q[{control_qubit_1}],q[{control_qubit_2}],q[{target_qubit}]);
        """

    def cswap(
        self, control_qubit_1: int, control_qubit_2: int, target_qubit: int
    ) -> None:
        self._validate_qubit_index(control_qubit_1)
        self._validate_qubit_index(control_qubit_2)
        self._validate_qubit_index(target_qubit)
        self._gates += f"""
        CSWAP(q[{control_qubit_1},q[{control_qubit_2}],q[{target_qubit}]);
        """
