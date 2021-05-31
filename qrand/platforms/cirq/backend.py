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
from cirq_google.engine import Engine 
from ..backend import QuantumBackend


###############################################################################
## CIRQ BACKEND (DECORATOR)
###############################################################################



class CirqBackend(QuantumBackend,Engine):
    """
    
        Encapsulating Google Engine API with Quantum Backend 

        Since API and Cirq is still in Alpha,Changes are expected
      
        methods from Engine class:

        create_program()->Wraps a Circuit for use with the Quantum Engine. i.e return engineprogram

        run()->Runs the supplied Circuit via Quantum Engine. i.e return study.result    
    """
    def __init__(
                self, 
                engine: Engine,
                shots:int =1,
                max_experiments:int=1
        ) -> None:
        self._backend: Engine = engine
        super(QuantumBackend, self).__init__(   )
        self._options = engine.service_args
        self._shots:int= shots,
        self._max_experiments = max_experiments
        self.max_shots=shots #Google API is still private 

    ############################### PUBLIC API ###############################
    @property
    def max_measurements(self) -> int:
        return  (self._max_experiments*self._shots )

    @property
    def max_experiments(self) -> int:
        return self._max_experiments
 
    @max_experiments.setter
    def max_experiments(self,max_experiments:int)->None:
        self._max_experiments:int=max_experiments

    """
    @property
    def max_qubits(self) -> int:
        return (
            
        )
    """

    #Using Consitent Qiskit analogy
    @property
    def shots(self) -> int:
        return self._shots

    @shots.setter
    def shots(self,shots:int) -> None:
        self._shots:int = shots

    def run(self, run_input, **options):
        return self._backend.run(run_input, self._shots,**options)