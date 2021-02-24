##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: February 22, 2021
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

from numpy.random import Generator  # type: ignore
from qiskit import IBMQ, BasicAer

from qrand import QiskitBitGenerator, __version__


###############################################################################
## VERSION
###############################################################################
def test_version():
    assert __version__ == "0.2.0"


###############################################################################
## IMPORTS
###############################################################################
def test_QiskitBitGenerator():
    provider = IBMQ.load_account()
    bitgen = QiskitBitGenerator(provider)
    assert not bitgen.state["backend_config"]["simulator"]
    simulator = BasicAer.get_backend("qasm_simulator")
    bitgen = QiskitBitGenerator(backend=simulator)
    assert bitgen.state["backend_config"]["simulator"]
    gen = Generator(bitgen)
    cache = "100" * 1000
    assert bitgen.load_cache(cache)
    assert (
        bitgen.random_raw() == 10540996613548315209
        and bitgen.random_bitstring()
        == "0010010010010010010010010010010010010010010010010010010010010010"
        and bitgen.random_uint() == 5270498306774157604
        and bitgen.random_double() == 0.5714285714285714
    )
    assert (
        gen.binomial(4, 1 / 4) == 0
        and gen.exponential() == 0.18350170297843915
        and gen.logistic() == 0.28768207245178085
        and gen.poisson() == 0
        and gen.standard_normal() == -0.24679872730094507
        and gen.triangular(-1, 0, 1) == 0.07417990022744847
    )
    assert bitgen.flush_cache()
    bitgen = QiskitBitGenerator(max_bits_per_request=128, ISRAW32=True)
    bitgen.random_raw()
    assert bitgen._fetch_random_bits()
