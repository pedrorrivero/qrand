##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: February 24, 2020
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
from qrand._qrng import Qrng


###############################################################################
## QRNG
###############################################################################
class TestBitCache:
    ############################# PUBLIC METHODS #############################
    def test_get_bit_string(self):
        bitgen = QiskitBitGenerator()
        bitgen32 = QiskitBitGenerator(ISRAW32=True)
        qrng = Qrng(bitgen)
        qrng32 = Qrng(bitgen32)
        cache = "100" * 1000
        bitgen.load_cache(cache)
        bitgen32.load_cache(cache)
        assert qrng.get_bit_string() == cache[:64]
        assert qrng32.get_bit_string() == cache[:32]
        assert qrng.get_bit_string(4) == cache[64:68]

    def test_get_random_complex_polar(self):
        bitgen = QiskitBitGenerator()
        qrng = Qrng(bitgen)
        cache = "100" * 1000
        bitgen.load_cache(cache)
        assert (
            qrng.get_random_complex_polar()
            == -0.16820993120165456 + 0.7369762251347793j
        )
        assert (
            qrng.get_random_complex_polar(4)
            == -1.362136709039319 - 0.6559701073130655j
        )
        assert (
            qrng.get_random_complex_polar(4, 3.14)
            == 1.926563627649004 + 0.9272437045189929j
        )

    def test_get_random_complex_rect(self):
        bitgen = QiskitBitGenerator()
        qrng = Qrng(bitgen)
        cache = "100" * 1000
        bitgen.load_cache(cache)
        assert (
            qrng.get_random_complex_rect()
            == 0.14285707473754883 - 0.4285714626312256j
        )
        assert (
            qrng.get_random_complex_rect(-4, 4)
            == -2.8571434020996094 + 0.5714282989501953j
        )
        assert (
            qrng.get_random_complex_rect(-4, 3, -2, 1)
            == -2.0000001192092896 - 1.5714287757873535j
        )

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
        cache = "100" * 1000
        bitgen.load_cache(cache)
        assert qrng.get_random_int() == 1
        assert qrng.get_random_int(-4, 4) == 0

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
        bitgen_state = qrng.state["qiskit_bit_generator"]
        assert bitgen_state["BITS"] == 64
        assert bitgen_state["job_config"] == job_config
        assert bitgen_state["backend_config"] == backend_config
        assert bitgen_state["bitcache"] == bitcache
