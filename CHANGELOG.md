## 0.3.0a0 (2021-05-12)

### Fix

- **QiskitBitGenerator**: move deprecation warning
- update qiskit version dependency
- platform-protocol circular dependency

### Feat

- add quantum_bit_generator

### Refactor

- **platforms**: rename quantum factory
- imports
- **platforms**: upgrade architecture
- **bit_cache**: extract BitCache to a separate module
- update package and module names
- **quantum_platforms**: update circuit and job models
- redesign architecture (preliminary)

### Perf

- **QiskitPlatform**: upgrade _compute_bounded_factorization

## 0.2.0 (2021-02-24)

### Feat

- **qrng**: add default parameter values

## 0.2.0b0 (2021-02-24)

### Refactor

- **qrng**: rename variable in get_random_float method
- **qrng**: arrange public methods in alphabetical order

### Feat

- **qrng**: add state property

## 0.2.0a0 (2021-02-23)

### Refactor

- rename qiskit_bit_generator module
- **qrng**: change internal bit_generator scope
- **qrng**: simplify get_random_int
- **qrng**: simplify get_random_int
- **qrng**: simplify get_random_double

### Feat

- **qrng**: add qrng class with base functionality

## 0.1.0 (2021-02-22)

### Refactor

- **qiskit_bitgenerator**: simplify QiskitBitGenerator._circuit

## 0.1.0a0 (2020-11-30)

### Refactor

- **qiskit_bitgenerator**: fix alphabetical ordering of methods
- **qiskit_bitgenerator**: rename bits to BITS, Final[int]
- **qiskit_bitgenerator**: methods by alphabetical order
- **qiskit_bitgenerator**: move n_qubits calc to job_partition
- **qiskit_bitgenerator**: rename get_random_* to random_*
- **qiskit_bitgenerator**: rename israw32 to ISRAW32 with type Final
- **qiskit_bitgenerator**: rename get_random_int to get_random_uint
- **qiskit_bitgenerator**: simplify get_random_double
- **qiskit_bitgenerator**: remove _state_getter and _state_setter
- **qiskit_bitgenerator**: move _memory property outside _config
- **qiskit_bitgenerator**: decouple dynamic_backend from provider
- **qiskit_bitgenerator**: make cls attribute DEFAULT_CONFIG private
- **qiskit_bitgenerator**: make attribute israw32 private
- **qiskit_bitgenerator**: rename methods in BitCache
- **qiskit_bitgenerator**: simplify static types
- **qiskit_bitgenerator**: add _parse_backend_config method
- **qiskit_bitgenerator**: add static types
- **qiskit_bitgenerator**: add static types

### Fix

- **qiskit_bitgenerator**: max_bits_per_request < backend_config.n_qubits
- **qiskit_bitgenerator**: partition_job method
- **qiskit_bitgenerator**: max_bits_per_request assignment
- **qiskit_bitgenerator**: new set_state

### Feat

- **qiskit_bitgenerator**: add bits_per_request to job_config
- **qiskit_bitgenerator**: import QiskitBitGenerator in qrand __init__
- **qiskit_bitgenerator**: add max_bits_per_request option
- **qiskit_bitgenerator**: add default n_bits to get_random_*
- **qiskit_bitgenerator**: add @state.setter functionality
- **qiskit_bitgenerator**: add set_state functionality
- **qiskit_bitgenerator**: upgrade to UserBitGenerator wrapper class
- **qiskit_bitgenerator**: add memory result parsing functionality
- **qiskit_bitgenerator**: add flush_cache functionality
- **qiskit_bitgenerator**: add dynamic backend update and filtering
- **qiskit_bitgenerator**: add dump_cache functionality
- **qiskit_bitgenerator**: add load_cache functionality
- **qiskit_bitgenerator**: expand QiskitBitGenerator.state property
- **qiskit_bitgenerator**: add get_random_double functionality
- **qiskit_bitgenerator**: add get_random_int functionality
- **qiskit_bitgenerator**: implement base functionality

## 0.0.1 (2020-10-13)

## 0.0.0 (2020-10-13)
