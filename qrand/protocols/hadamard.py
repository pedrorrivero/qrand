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

from typing import List, Literal, Optional, Tuple

from ..helpers import (
    ALPHABETS,
    compute_bounded_factorization,
    validate_natural,
    validate_numeral,
    validate_type,
)
from ..platforms import (
    QuantumBackend,
    QuantumCircuit,
    QuantumFactory,
    QuantumJob,
)
from .protocol import BareQuantumProtocol
from .result import BasicResult


###############################################################################
## HADAMARD PROTOCOL
###############################################################################
class HadamardProtocol(BareQuantumProtocol):
    """
    Simple QRNG protocol based on applying Hadamard gates to all qubits.

    Parameters
    ----------
    max_bits: int, optional
        The maximum number of usable bits to retrieve.

    Attributes
    ----------
    max_bits: int, optional
        The maximum number of usable bits to retrieve.

    Methods
    -------
    run(factory: QuantumFactory) -> BasicResult
        Run QRNG protocol.
    verify() -> Literal[False]
        Verify protocol execution.
    """

    def __init__(self, max_bits: Optional[int] = None) -> None:
        self.max_bits: Optional[int] = max_bits

    ############################### PUBLIC API ###############################
    @property
    def max_bits(self) -> Optional[int]:
        """
        The maximum number of bits to retrieve.
        """
        return self._max_bits

    @max_bits.setter
    def max_bits(self, max_bits: Optional[int]) -> None:
        if max_bits is not None:
            validate_natural(max_bits, zero=False)
        self._max_bits: Optional[int] = max_bits

    def run(self, factory: QuantumFactory) -> BasicResult:
        validate_type(factory, QuantumFactory)
        backend: QuantumBackend = factory.retrieve_backend()
        num_qubits, num_measurements = self._partition_job(backend)
        circuit: QuantumCircuit = factory.create_circuit(num_qubits)
        self._assemble_quantum_circuit(circuit)
        job: QuantumJob = factory.create_job(
            circuit, backend, num_measurements
        )
        measurements: List[str] = job.execute()
        return self._parse_measurements(measurements)

    def verify(self) -> Literal[False]:
        return False

    ############################### PRIVATE API ###############################
    @staticmethod
    def _assemble_quantum_circuit(circuit: QuantumCircuit) -> None:
        validate_type(circuit, QuantumCircuit)
        for q in range(circuit.num_qubits):
            circuit.h(q)
            circuit.measure(q)

    def _parse_measurements(self, measurements: List[str]) -> BasicResult:
        validate_type(measurements, list)
        bitstring: str = ""
        for m in measurements:
            validate_numeral(m, ALPHABETS["BINARY"])
            bitstring += m
        return BasicResult(bitstring)

    def _partition_job(self, backend: QuantumBackend) -> Tuple[int, int]:
        validate_type(backend, QuantumBackend)
        return (
            compute_bounded_factorization(
                self.max_bits, backend.max_qubits, backend.max_measurements
            )
            if self.max_bits
            else (backend.max_qubits, backend.max_measurements)
        )
