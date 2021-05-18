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

from typing import Callable, Optional

from qiskit.providers import BackendV1 as Backend
from qiskit.providers import Job, Options

from ..backend import QuantumBackend


###############################################################################
## QISKIT BACKEND (DECORATOR)
###############################################################################
class QiskitBackend(QuantumBackend, Backend):
    def __init__(
        self, backend: Backend, max_bits_per_request: Optional[int] = None
    ) -> None:
        self._base_backend: Backend = backend
        super(QuantumBackend, self).__init__(
            backend.configuration(), backend.provider()
        )
        self._options: Options = backend._options
        try:
            mbpr = backend.max_bits_per_request
        except AttributeError:
            mbpr = None
        self.max_bits_per_request = max_bits_per_request or mbpr

    ############################### PUBLIC API ###############################
    @property
    def configuration_dict(self) -> dict:
        return self.configuration().to_dict()

    @property
    def max_experiments(self) -> int:
        return (
            self.configuration_dict["max_experiments"]
            if self.configuration_dict.__contains__("max_experiments")
            and self.configuration_dict["max_experiments"]
            else 1
        )

    @property
    def max_measurements(self) -> int:
        return self.max_shots * self.max_experiments

    @property
    def max_qubits(self) -> int:
        return (
            self.configuration_dict["num_qubits"]
            if self.configuration_dict.__contains__("num_qubits")
            and self.configuration_dict["num_qubits"]
            else 1
        )

    @property
    def max_shots(self) -> int:
        return (
            self.configuration_dict["max_shots"]
            if self.configuration_dict.__contains__("max_shots")
            and self.configuration_dict["max_shots"]
            and self.memory
            else 1
        )

    @property
    def memory(self) -> bool:
        return (
            self.configuration_dict["memory"]
            if self.configuration_dict.__contains__("memory")
            else False
        )

    ############################ QISKIT INTERFACE ############################
    def _default_options(self) -> Options:
        return self._base_backend._default_options()

    def run(self, run_input, **options) -> Job:
        return self._base_backend.run(run_input, **options)
