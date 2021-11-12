##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: May 17, 2021
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


from typing import List, Optional
from warnings import warn



from ...helpers import compute_bounded_factorization, reverse_endian
from ..job import QuantumJob
from .backend import CirqBackend
from .circuit import CirqCircuit


###############################################################################
## CIRQ JOB
###############################################################################
class CirqJob(QuantumJob):
    def __init__(
        self,
        circuit:CirqCircuit,
        backend:CirqBackend,
        num_measurements:Optional[int]=None
    ) -> None:
        self.backend:CirqBackend = backend
        self.circuit:CirqCircuit = circuit
        self.num_measurements:int = num_measurements
        
        

    ############################### PUBLIC API ###############################
    @property
    def backend(self) -> CirqBackend:
        return self._backend 

    @backend.setter
    def backend(self, backend: CirqBackend) -> None:
        self._backend: CirqBackend = backend

    @property
    def circuit(self) -> CirqCircuit:
        return self._circuit

    @circuit.setter
    def circuit(self, circuit: CirqCircuit) -> None:
        self._circuit: CirqCircuit = circuit

    @property
    def num_measurements(self) -> int:
        return self._shots

    @num_measurements.setter
    def num_measurements(self, num_measurements: Optional[int]) -> None:
          #Shots == Reptition....Used because of Qiskit analogy in whole qrand
           num_measurements = (
            num_measurements
            if isinstance(num_measurements, int) and 0 < num_measurements
            else self.backend.max_measurements
        )
           if  self.backend.max_measurements < num_measurements:
            warn(
                f"Number of measurements unsupported by the job's Backend: \
                {self.backend.max_measurements}<{num_measurements}. \
                Using max_measurements instead.",
                UserWarning,
            )
            num_measurements=self._backend.max_measurements
            self._shots, self._experiments = compute_bounded_factorization(
            num_measurements,
            self.backend.max_shots,
            self.backend.max_experiments,
        )

    def execute(self) -> List[str]:
        self.cirqcirc=self._circuit.createcircuit()
        return self._backend.run(self.cirqcirc)