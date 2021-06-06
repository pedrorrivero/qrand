##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: June 6, 2021
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

from .backend import QuantumBackend
from .circuit import QuantumCircuit
from .factory import QuantumFactory
from .job import QuantumJob
from .platform import QuantumPlatform

__all__ = [
    "QuantumBackend",
    "QuantumCircuit",
    "QuantumFactory",
    "QuantumJob",
    "QuantumPlatform",
]


###############################################################################
## CIRQ IMPORT
###############################################################################
__cirq__ = True
__all__ += "__cirq__"
try:
    from .cirq import CirqBackend, CirqCircuit, CirqJob, CirqPlatform
except ImportError:
    __cirq__ = False
else:
    __all__ += [
        "CirqBackend",
        "CirqCircuit",
        "CirqJob",
        "CirqPlatform",
    ]


###############################################################################
## QISKIT IMPORT
###############################################################################
__qiskit__ = True
__all__ += "__qiskit__"
try:
    from .qiskit import QiskitBackend, QiskitCircuit, QiskitJob, QiskitPlatform
except ImportError:
    __qiskit__ = False
else:
    __all__ += [
        "QiskitBackend",
        "QiskitCircuit",
        "QiskitJob",
        "QiskitPlatform",
    ]


###############################################################################
## QSHARP IMPORT
###############################################################################
__qsharp__ = True
__all__ += "__qsharp__"
try:
    from .qsharp import QsharpBackend, QsharpCircuit, QsharpJob, QsharpPlatform
except Exception:  # qsharp also requires the IQ# kernel
    __qsharp__ = False
else:
    __all__ += [
        "QsharpBackend",
        "QsharpCircuit",
        "QsharpJob",
        "QsharpPlatform",
    ]
