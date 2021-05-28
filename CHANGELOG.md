## 0.3.0a6 (2021-05-27)

### Refactor

- **helpers**: merge numeral encoding functions in one module
- **Qrng**: update get_complex_rect argument defaults
- **Qrng**: convert to class wrapper [issue #14]
- **Qrng**: redesign get_random_base32 and get_random_base64
- **QuantumBitGenerator**: remove argument checks in random_uint
- **reverse_endian**: rename bitstrings to numerals
- **HadamardProtocol**: rename output to measurements
- **Qrng**: reorder in public and private API

### Fix

- **ValidationDecorator**: fix BareQuantumProtocol instance check
- **QuantumBitGenerator**: verify attribute types on set

### Feat

- **QuantumBitGenerator**: add default protocol [issue #14]
- **Qrng**: add get_random_string
- **Qrng**: add quantum_bit_generator property

### Perf

- **Qrng**: minimize bit consumption in get_random_float
- **QuantumBitGenerator**: minimize bit consumption in random_uint

## 0.3.0a5 (2021-05-20)

### Refactor

- **platforms**: remove unnecessary type ignore tags
- **QuantumBitGenerator**: random bitstring and uint signature
- **HadamardProtocol**: update private API signatures
- restrict max_bits attribute to protocols

### Feat

- **compute_bounded_factorization**: add argument validation

## 0.3.0a4 (2021-05-19)

### Refactor

- **ValidationDecorator**: remove validation_strategy setter
- **platforms**: extract max_bits_per_request from QuantumBackend
- **QuantumBitGenerator**: introduce BitCache interface

### Feat

- **QuantumBitGenerator**: add max_bits_per_request attribute
- **QuantumBitGenerator**: add bitcache attribute
- **errors**: add raise_deprecation_warning

### Fix

- **platforms**: update QuantumPlatform fetch_random_bits signature

## 0.3.0a3 (2021-05-18)

### Feat

- **platforms**: new gates for quantum circuits

### Refactor

- **caches**: move BitCache to caches subpackage
- **protocols**: rename PlaintResult to BasicResult
- **helpers**: add is_bitstring
- **reverse_endian**: rename argument

## 0.3.0a2 (2021-05-17)

### Feat

- **helpers**: add reverse_endian
- **Qrng**: add get_random_uint
- **Qrng**: add get_random_decimal
- **Qrng**: add get_random_bytes
- **Qrng**: add random OCTAL, HEX, BASE32, and BASE64

### Refactor

- **platforms**: update QiskitJob constructor
- **platforms**: extract QuantumBackend from QuantumJob
- **Qrng**: rename get_bit_string to get_random_bitstring
- **Qrng**: order methods alphabetically
- **Qrng**: order methods alphabetically
- **Qrng**: clean-up base32, base64, hex and octal

### Fix

- **Qrng**: reimplement get_bit_string with deprecation warning
- **Qrng**: set default num_bits in get_random_bytes
- **Qrng**: replace decode for encode in b32 and b64
- **Qrng**: update output types in base32 and base64
- **Qrng**: update random complex precision to double

### Perf

- **Qrng**: simplify imports

## 0.3.0a1 (2021-05-13)

### Refactor

- **protocols**: rename stream to measurement
- **protocols**: rename SimpleResult to PlainResult
- **platforms**: change job output to list of measurements
- rename repetitions to num_measurements

### Fix

- **QiskitJob**: update error and warning messages

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
