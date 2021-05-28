##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: May 25, 2021
##   | |    | | \ \    ---------------------------------
##   |_|    |_|  \_\   https://github.com/pedrorrivero
##

## Copyright 2020 Pedro Rivero
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

from qrand import QiskitBitGenerator
from qrand.qrng import Qrng


###############################################################################
## QRNG
###############################################################################
class TestBitCache:
    ############################# PUBLIC METHODS #############################
    # def test_get_random_bitstring(self):
    #     bitgen = QiskitBitGenerator()
    #     bitgen32 = QiskitBitGenerator(ISRAW32=True)
    #     qrng = Qrng(bitgen)
    #     qrng32 = Qrng(bitgen32)
    #     cache = "100" * 1000
    #     bitgen.load_cache(cache)
    #     bitgen32.load_cache(cache)
    #     assert qrng.get_random_bitstring() == cache[:64]
    #     assert qrng32.get_random_bitstring() == cache[:32]
    #     assert qrng.get_random_bitstring(4) == cache[64:68]

    # def test_get_random_complex_polar(self):
    #     bitgen = QiskitBitGenerator()
    #     qrng = Qrng(bitgen)
    #     cache = "100" * 1000
    #     bitgen.load_cache(cache)
    #     assert (
    #         qrng.get_random_complex_polar()
    #         == 0.4713139887723277 + 0.5910090485061033j
    #     )
    #     assert (
    #         qrng.get_random_complex_polar(4)
    #         == -1.9263524684802522 - 0.9276824556973191j
    #     )
    #     assert (
    #         qrng.get_random_complex_polar(4, 3.14)
    #         == 0.9431657500378959 + 1.1815890375548252j
    #     )
    #
    # def test_get_random_complex_rect(self):
    #     bitgen = QiskitBitGenerator()
    #     qrng = Qrng(bitgen)
    #     cache = "100" * 1000
    #     bitgen.load_cache(cache)
    #     assert (
    #         qrng.get_random_complex_rect()
    #         == 0.1428571428571428 - 0.7142857142857144j
    #     )
    #     assert (
    #         qrng.get_random_complex_rect(-4, 4)
    #         == -1.7142857142857153 + 0.5714285714285712j
    #     )
    #     assert (
    #         qrng.get_random_complex_rect(-4, 3, -2, 1)
    #         == -3.0000000000000004 - 1.1428571428571432j
    #     )

    def test_get_random_double(self):
        bitgen = QiskitBitGenerator()
        qrng = Qrng(bitgen)
        cache = "100" * 1000
        bitgen.load_cache(cache)
        assert qrng.get_random_double() == 0.1428571428571428
        assert qrng.get_random_double(-4, 4) == -2.8571428571428577

    def test_get_random_float(self):
        bitgen = QiskitBitGenerator()
        qrng = Qrng(bitgen)
        cache = "100" * 1000
        bitgen.load_cache(cache)
        assert qrng.get_random_float() == 0.14285707473754883
        assert qrng.get_random_float(-4, 4) == -1.7142858505249023

    def test_get_random_int(self):
        bitgen = QiskitBitGenerator()
        qrng = Qrng(bitgen)
        cache = "001" * 1000
        bitgen.load_cache(cache)
        assert qrng.get_random_int() == -1
        assert qrng.get_random_int(-4, 4) == -2

    def test_get_random_int32(self):
        bitgen = QiskitBitGenerator()
        qrng = Qrng(bitgen)
        cache = "100" * 1000
        bitgen.load_cache(cache)
        assert qrng.get_random_int32() == 2454267026

    def test_get_random_int64(self):
        bitgen = QiskitBitGenerator()
        qrng = Qrng(bitgen)
        cache = "100" * 1000
        bitgen.load_cache(cache)
        assert qrng.get_random_int64() == 10540996613548315209

    def test_state(self):
        bitgen = QiskitBitGenerator()
        qrng = Qrng(bitgen)
        cache = "100" * 1000
        bitgen.load_cache(cache)
        job_config = {
            "max_bits_per_request": None,
            "bits_per_request": 1572864,
            "n_qubits": 24,
            "shots": 65536,
            "experiments": 1,
        }
        backend_config = {
            # "backend_name": "qasm_simulator",
            "credits_required": False,
            "local": True,
            "n_qubits": 24,
            "simulator": True,
        }
        bitcache = {
            "size": 3000,
        }
        bitgen_state = qrng.state["quantum_bit_generator"]
        assert bitgen_state["BITS"] == 64
        assert bitgen_state["job_config"] == job_config
        assert bitgen_state["backend_config"] == backend_config
        assert bitgen_state["bitcache"] == bitcache
