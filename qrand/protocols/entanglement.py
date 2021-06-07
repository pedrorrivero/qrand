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
## ENTANGLEMENT PROTOCOL
###############################################################################
class EntanglementProtocol(BareQuantumProtocol):
    """
    QRNG protocol with entanglement for public randomness testing [1]_.

    Simple idealistic quantum entanglement based protocol for quantum random
    number generation allowing a trusted third party to publicly perform
    arbitrarily complex tests of randomness without any violation of the
    secrecy of the generated bit sequences. The protocol diminishes also an
    average time of the randomness testing (thus enabling arbitrary shortening
    of this time with increasing number of entangled qubits).

    Parameters
    ----------
    max_bits: int, optional
        The maximum number of usable bits to retrieve.
    purify: bool, default: True
        Whether to discard odd parity measurements (even parity expected).

    Attributes
    ----------
    max_bits: int, optional
        The maximum number of usable bits to retrieve.
    purify: bool
        Whether to discard odd parity measurements (even parity expected).

    Methods
    -------
    run(factory: QuantumFactory) -> BasicResult
        Run QRNG protocol.
    verify() -> Literal[False]
        Verify protocol execution.

    References
    ----------
    .. [1] Jacak, J.E., Jacak, W.A., Donderowicz, W.A. et al. Quantum random
        number generators with entanglement for public randomness testing.
        Sci Rep 10, 164 (2020). https://doi.org/10.1038/s41598-019-56706-2
    """

    def __init__(
        self, max_bits: Optional[int] = None, purify: bool = True
    ) -> None:
        self.max_bits: Optional[int] = max_bits
        self.purify: bool = purify

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

    @property
    def purify(self) -> bool:
        """
        Whether to discard odd parity measurements (even parity expected).
        """
        return self._purify

    @purify.setter
    def purify(self, purify: bool) -> None:
        validate_type(purify, bool)
        self._purify: bool = purify

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
        for q in range(1, circuit.num_qubits):
            circuit.h(q)
            circuit.cx(q, 0)
            circuit.measure(q)
        circuit.measure(0)

    @staticmethod
    def _check_even_parity(measurement: str) -> bool:
        return measurement.count("1") % 2 == 0

    def _parse_measurements(self, measurements: List[str]) -> BasicResult:
        validate_type(measurements, list)
        num_bits = len(measurements[0])
        num_sequences = num_bits - 1
        bit_sequences: List[str] = [""] * num_sequences
        for m in measurements:
            validate_numeral(m, ALPHABETS["BINARY"])
            if self.purify and not self._check_even_parity(m):
                continue
            for b in range(num_sequences):
                bit_sequences[b] += m[b]
        bitstring: str = ""
        validation_token: str = bit_sequences.pop(0)
        for s in bit_sequences:
            bitstring += s
        return BasicResult(bitstring, validation_token)

    def _partition_job(self, backend: QuantumBackend) -> Tuple[int, int]:
        validate_type(backend, QuantumBackend)
        if backend.max_qubits < 3:
            raise RuntimeError(
                f"EntanglementProtocol needs at least three qubits to run. \
                Retreived backend can only handle {backend.max_qubits} < 3."
            )
        if self.max_bits:
            num_qubits: int = min(self.max_bits + 2, backend.max_qubits)
            num_measurements: int = self.max_bits // (num_qubits - 2)
            return num_qubits, min(num_measurements, backend.max_measurements)
        return backend.max_qubits, backend.max_measurements
