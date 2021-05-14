##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: May 13, 2021
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

import pytest
from numpy import float64, uint32, uint64
from qiskit import IBMQ, BasicAer, QuantumCircuit, execute
from qiskit.providers import Backend, Job, Provider
from qiskit.providers.ibmq import IBMQError, least_busy
from qiskit.providers.models import BackendConfiguration
from qiskit.result import Counts, Result
from randomgen import UserBitGenerator

from qrand._qiskit_bit_generator import BitCache, QiskitBitGenerator


###############################################################################
## BIT CACHE
###############################################################################
class TestBitCache:
    ########################## STATIC/CLASS METHODS ##########################
    def test_isbitstring(self):
        bitcache = BitCache()
        with pytest.raises(TypeError):
            bitcache.isbitstring(4)
        assert not bitcache.isbitstring("abc")
        assert bitcache.isbitstring("100")

    ############################# PUBLIC METHODS #############################
    def test_dump(self):
        bitcache = BitCache()
        cache = "100" * 100
        bitcache.push(cache)
        assert bitcache.dump() == cache

    def test_flush(self):
        bitcache = BitCache()
        cache = "100" * 100
        bitcache.push(cache)
        assert (
            bitcache.flush() and bitcache.size == 0 and bitcache.dump() == ""
        )

    def test_pop(self):
        bitcache = BitCache()
        cache = "100" * 100
        bitcache.push(cache)
        with pytest.raises(ValueError):
            bitcache.pop(0)
        with pytest.raises(ValueError):
            bitcache.pop(-1)
        with pytest.raises(ValueError):
            bitcache.pop(len(cache) + 1)
        assert (
            bitcache.pop(3) == "100"
            and bitcache._cache == cache[3:]
            and bitcache.size == len(cache) - 3
        )
        assert (
            bitcache.pop(len(cache) - 3) == cache[3:]
            and bitcache._cache == ""
            and bitcache.size == 0
        )

    def test_push(self):
        bitcache = BitCache()
        cache = "100" * 100
        with pytest.raises(TypeError):
            bitcache.push(0)
        with pytest.raises(ValueError):
            bitcache.push("abc")
        assert (
            bitcache.push(cache)
            and bitcache._cache == cache
            and bitcache.size == len(cache)
        )

    ############################ PUBLIC PROPERTIES ############################
    def test_state(self):
        bitcache = BitCache()
        cache = "100" * 100
        bitcache.push(cache)
        assert bitcache.state == {"size": len(cache)}


###############################################################################
## QISKIT BIT GENERATOR
###############################################################################
class TestQiskitBitGenerator:
    ########################## STATIC/CLASS METHODS ##########################
    # def test_default_backend_filter(self):
    #     provider = IBMQ.load_account()
    #     simulator = BasicAer.get_backend("qasm_simulator")
    #     assert not QiskitBitGenerator.default_backend_filter(simulator)
    #     assert not (
    #         no_memory := provider.backends(
    #             filters=lambda b: not b.configuration().memory
    #             and not b.configuration().simulator
    #         )
    #     ) or not QiskitBitGenerator.default_backend_filter(no_memory[0])
    #     assert (
    #         backend := provider.backends(
    #             filters=lambda b: b.configuration().memory
    #             and not b.configuration().simulator
    #         )
    #     ) and QiskitBitGenerator.default_backend_filter(backend[0])

    # def test_get_best_backend(self):
    #     provider = IBMQ.load_account()
    #     assert QiskitBitGenerator.get_best_backend(provider)
    #
    #     def filter(b):
    #         if b.configuration().backend_name == "ibmq_qasm_simulator":
    #             return True
    #         else:
    #             return False
    #
    #     backend = QiskitBitGenerator.get_best_backend(provider, filter)
    #     assert backend.configuration().backend_name == "ibmq_qasm_simulator"
    #     with pytest.raises(IBMQError):
    #         QiskitBitGenerator.get_best_backend(provider, lambda b: False)

    ############################# PUBLIC METHODS #############################
    def test_dump_cache(self):
        bitgen = QiskitBitGenerator()
        cache = "100" * 100
        bitgen.load_cache(cache)
        assert bitgen.dump_cache() == cache
        assert (
            bitgen.dump_cache(flush=True) == cache
            and bitgen._bitcache.size == 0
            and bitgen._bitcache._cache == ""
        )

    def test_flush_cache(self):
        bitgen = QiskitBitGenerator()
        cache = "100" * 100
        bitgen.load_cache(cache)
        assert (
            bitgen.flush_cache()
            and bitgen._bitcache.size == 0
            and bitgen._bitcache._cache == ""
        )

    def test_load_cache(self):
        bitgen = QiskitBitGenerator()
        cache = "100" * 100
        with pytest.raises(TypeError):
            bitgen.load_cache(0)
        with pytest.raises(ValueError):
            bitgen.load_cache("abc")
        assert (
            bitgen.load_cache(cache)
            and bitgen.load_cache(cache)
            and bitgen._bitcache.size == 2 * len(cache)
            and bitgen._bitcache._cache == cache + cache
        )
        assert (
            bitgen.load_cache(cache, flush=True)
            and bitgen._bitcache.size == len(cache)
            and bitgen._bitcache._cache == cache
        )

    def test_random_bitstring(self):
        bitgen = QiskitBitGenerator()
        cache = "100" * 100
        n_bits = 4
        bitgen.load_cache(cache)
        assert (
            bitgen.random_bitstring(-1) == cache[: bitgen.BITS]
            and bitgen.random_bitstring(0)
            == cache[bitgen.BITS : bitgen.BITS * 2]
            and bitgen.random_bitstring(n_bits)
            == cache[bitgen.BITS * 2 : bitgen.BITS * 2 + n_bits]
        )
        bitgen = QiskitBitGenerator(ISRAW32=True)
        cache = "100" * 100
        n_bits = 4
        bitgen.load_cache(cache)
        assert (
            bitgen.random_bitstring(-1) == cache[: bitgen.BITS]
            and bitgen.random_bitstring(0)
            == cache[bitgen.BITS : bitgen.BITS * 2]
            and bitgen.random_bitstring(n_bits)
            == cache[bitgen.BITS * 2 : bitgen.BITS * 2 + n_bits]
        )

    def test_random_double(self):
        bitgen = QiskitBitGenerator()
        cache = "100" * 100
        n = 4
        bitgen.load_cache(cache)
        assert (
            bitgen.random_double(-1) == -0.5714285714285714
            and bitgen.random_double(0) == 0.0
            and bitgen.random_double(n) == 1.1428571428571423
        )
        bitgen = QiskitBitGenerator(ISRAW32=True)
        cache = "100" * 100
        n = 4
        bitgen.load_cache(cache)
        assert (
            bitgen.random_double(-1) == -0.5714285714285714
            and bitgen.random_double(0) == 0.0
            and bitgen.random_double(n) == 1.1428571428571423
        )

    def test_random_uint(self):
        bitgen = QiskitBitGenerator()
        cache = "100" * 100
        n_bits = 4
        bitgen.load_cache(cache)
        assert (
            bitgen.random_uint(-1) == 10540996613548315209
            and bitgen.random_uint(0) == 2635249153387078802
            and bitgen.random_uint(n_bits) == 4
        )
        bitgen = QiskitBitGenerator(ISRAW32=True)
        cache = "100" * 100
        n_bits = 4
        bitgen.load_cache(cache)
        assert (
            bitgen.random_uint(-1) == 2454267026
            and bitgen.random_uint(0) == 1227133513
            and bitgen.random_uint(n_bits) == 2
        )

    # def test_set_state(self):
    #     provider = IBMQ.load_account()
    #     simulator = BasicAer.get_backend("qasm_simulator")
    #     bitgen = QiskitBitGenerator()
    #     assert not bitgen.set_state()
    #     assert bitgen.set_state(backend_filter=lambda b: True)
    #     assert bitgen.set_state(max_bits_per_request=400)
    #     assert bitgen.set_state(backend=simulator)
    #     assert bitgen.set_state(provider=provider)

    ############################# PRIVATE METHODS #############################
    # def test_fetch_random_bits(self):
    #     pass ## TODO!!!

    def test_parse_backend_config(self):
        bitgen = QiskitBitGenerator()
        MASK = bitgen._BACKEND_CONFIG_MASK
        backend_config = {
            "backend_name": "TEST",
            "simulator": True,
            "dummy_1": True,
            "dummy_2": 2,
            "dummy_3": 0.4,
            "dummy_4": "test",
            "dummy_5": None,
        }
        parsed_bc = bitgen._parse_backend_config(backend_config)
        MASK.pop("backend_name")
        assert parsed_bc.pop("backend_name") == "TEST" and parsed_bc == MASK

    # def test_parse_result(self):
    #     pass ## TODO!!!

    def test_set_mbpr(self):
        bitgen = QiskitBitGenerator()
        assert bitgen._set_mbpr(-1) and bitgen._max_bits_per_request == 0
        assert bitgen._set_mbpr(0) and bitgen._max_bits_per_request == 0
        assert bitgen._set_mbpr(1) and bitgen._max_bits_per_request == 1

    ############################ PUBLIC PROPERTIES ############################
    def test_BITS(self):
        bitgen64 = QiskitBitGenerator()
        bitgen32 = QiskitBitGenerator(ISRAW32=True)
        assert bitgen32.BITS == 32 and bitgen64.BITS == 64

    def test_state(self):
        bitgen = QiskitBitGenerator()
        state = {
            "BITS": 64,
            "backend_config": {
                # "backend_name": "qasm_simulator",
                "credits_required": False,
                "local": True,
                "n_qubits": 24,
                "simulator": True,
            },
            "bitcache": {"size": 0},
            "job_config": {
                "bits_per_request": 1572864,
                "experiments": 1,
                "max_bits_per_request": None,
                "n_qubits": 24,
                "shots": 65536,
            },
        }
        assert bitgen.state == state

    # def test_state_setter(self):
    #     provider = IBMQ.load_account()
    #     backend = QiskitBitGenerator.get_best_backend(provider)
    #     bitgen = QiskitBitGenerator()
    #     bitgen.state = {}
    #     assert bitgen.state == QiskitBitGenerator().state
    #     bitgen.state = {"backend_filter": lambda b: True}
    #     bitgen.state = {"max_bits_per_request": 400}
    #     assert bitgen.state["job_config"]["max_bits_per_request"] == 400
    #     bitgen.state = {"backend": backend}
    #     assert not bitgen.state["backend_config"]["simulator"]
    #     bitgen.state = {"provider": provider}
    #     assert not bitgen.state["backend_config"]["simulator"]

    ########################### PRIVATE PROPERTIES ###########################
    def test_backend_config(self):
        bitgen = QiskitBitGenerator()
        bc = BasicAer.get_backend("qasm_simulator").configuration().to_dict()
        assert bitgen._backend_config == bc

    def test_circuit(self):
        bitgen = QiskitBitGenerator()
        bc = bitgen._circuit
        n_qubits = bitgen._n_qubits
        assert (
            bc.num_qubits == n_qubits
            and bc.num_clbits == n_qubits
            and bc.size() == 2 * n_qubits
        )

    # def test_experiments(self):
    #     pass ## TODO!!!

    def test_job_config(self):
        bitgen = QiskitBitGenerator()
        bjc = bitgen._job_config
        jc = {
            "experiments": 1,
            "max_bits_per_request": None,
            "n_qubits": 24,
            "shots": 65536,
        }
        jc["bits_per_request"] = (
            jc["experiments"] * jc["shots"] * jc["n_qubits"]
        )
        assert bjc == jc and (
            not bjc["max_bits_per_request"]
            or bjc["max_bits_per_request"] >= bjc["bits_per_request"]
        )

    def test_job_partition(self):
        bitgen = QiskitBitGenerator()
        assert bitgen._job_partition == (24, 65536, 1)
        bitgen.state = {"max_bits_per_request": 4}
        assert bitgen._job_partition == (4, 1, 1)

    def test_memory(self):
        bitgen = QiskitBitGenerator()
        assert bitgen._backend_config["memory"] or not bitgen._memory
        memory = True if bitgen._n_qubits > 1 else False
        assert bitgen._memory == memory

    # def test_n_qubits(self):
    #     pass ## TODO!!!

    # def test_shots(self):
    #     pass ## TODO!!!

    ############################# NUMPY INTERFACE #############################
    # def test_next_raw(self):
    #     pass ## TODO!!!

    # def test_next_32(self):
    #     pass ## TODO!!!

    # def test_next_64(self):
    #     pass ## TODO!!!

    # def test_next_double(self):
    #     pass ## TODO!!!
