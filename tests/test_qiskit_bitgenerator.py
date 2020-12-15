##    _____  _____
##   |  __ \|  __ \    AUTHOR: Pedro Rivero
##   | |__) | |__) |   ---------------------------------
##   |  ___/|  _  /    DATE: December 15, 2020
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
from qiskit import (
    IBMQ,
    BasicAer,
    ClassicalRegister,
    QuantumCircuit,
    QuantumRegister,
    execute,
)
from qiskit.providers import Backend, Job, Provider
from qiskit.providers.ibmq import IBMQError, least_busy
from qiskit.providers.models import BackendConfiguration
from qiskit.result import Counts, Result
from randomgen import UserBitGenerator

from qrand._qiskit_bitgenerator import BitCache, QiskitBitGenerator

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
    def test_default_backend_filter(self):
        provider = IBMQ.load_account()
        simulator = BasicAer.get_backend("qasm_simulator")
        assert not QiskitBitGenerator.default_backend_filter(simulator)
        assert not (
            no_memory := provider.backends(
                filters=lambda b: not b.configuration().memory
                and not b.configuration().simulator
            )
        ) or not QiskitBitGenerator.default_backend_filter(no_memory[0])
        assert (
            backend := provider.backends(
                filters=lambda b: b.configuration().memory
                and not b.configuration().simulator
            )
        ) and QiskitBitGenerator.default_backend_filter(backend[0])

    # def test_get_best_backend(self):
    #     pass ## TODO!!!

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

    # def test_random_double(self):
    #     pass ## TODO!!!
    #
    # def test_random_uint(self):
    #     pass ## TODO!!!
    #
    # def test_set_state(self):
    #     pass ## TODO!!!

    ############################# PRIVATE METHODS #############################
    # def test_fetch_random_bits(self):
    #     pass ## TODO!!!
    #
    # def test_parse_backend_config(self):
    #     pass ## TODO!!!
    #
    # def test_parse_result(self):
    #     pass ## TODO!!!
    #
    # def test_set_mbpr(self):
    #     pass ## TODO!!!

    ############################ PUBLIC PROPERTIES ############################
    # def test_BITS(self):
    #     pass ## TODO!!!
    #
    # def test_state(self):
    #     pass ## TODO!!!

    ########################### PRIVATE PROPERTIES ###########################
    # def test_backend_config(self):
    #     pass ## TODO!!!
    #
    # def test_circuit(self):
    #     pass ## TODO!!!
    #
    # def test_experiments(self):
    #     pass ## TODO!!!
    #
    # def test_job_config(self):
    #     pass ## TODO!!!
    #
    # def test_job_partition(self):
    #     pass ## TODO!!!
    #
    # def test_memory(self):
    #     pass ## TODO!!!
    #
    # def test_n_qubits(self):
    #     pass ## TODO!!!
    #
    # def test_shots(self):
    #     pass ## TODO!!!

    ############################# NUMPY INTERFACE #############################
    # def test_next_raw(self):
    #     pass ## TODO!!!
    #
    # def test_next_32(self):
    #     pass ## TODO!!!
    #
    # def test_next_64(self):
    #     pass ## TODO!!!
    #
    # def test_next_double(self):
    #     pass ## TODO!!!
