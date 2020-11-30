[![Unitary Fund](https://img.shields.io/badge/Supported_By-UNITARY_FUND-FFF000.svg?style=flat)](http://unitary.fund)
[![YouTube](https://img.shields.io/badge/PR-qrand-FF0000.svg?style=flat&logo=YouTube&logoColor=white)](https://youtu.be/CG7BxuWFpME)
[![PyPI](https://img.shields.io/pypi/v/qrand?label=PyPI&style=flat&color=3776AB&logo=Python&logoColor=white)](https://pypi.org/project/qrand/)
[![MIT License](https://img.shields.io/github/license/pedrorrivero/qrand?label=License&style=flat&color=1D1D1D)](https://github.com/pedrorrivero/qrand/blob/master/LICENSE)


# qrand

> A quantum random number generator for arbitrary probability distributions

Random numbers are everywhere.

Computer algorithms, data encryption, physical simulations, and even the arts use them all the time. There is one problem though: it turns out that they are actually very difficult to produce in large amounts. Classical computers can only implement mathematical tricks to emulate randomness, while measuring it out of physical processes turns out to be too slow.

Luckily, the probabilistic nature of quantum computers makes these devices particularly useful for the task. Nonetheless, most of the current efforts in producing quantum random numbers have been focused on uniform probability distributions. Despite this fact, many applications actually need to sample from more complex distributions (e.g. gaussian, poisson).

This software introduces an interface layer between [NumPy](https://numpy.org/) and [Qiskit](https://qiskit.org/), along with some useful functionality that enables the production of quantum random numbers (QRN) for a wide variety of probability distributions. This is ultimately accomplished by transforming uniform probability distributions produced in IBMQ's quantum devices, through NumPy's random module.

```python3
from qrand import QiskitBitGenerator
from numpy.random import Generator
from qiskit import IBMQ

provider = IBMQ.load_account()
bitgen = QiskitBitGenerator(provider)
gen = Generator(bitgen)

print(f"Random Raw: {bitgen.random_raw()}")
print(f"Random Bitstring: {bitgen.random_bitstring()}")
print(f"Random Unsigned Int: {bitgen.random_uint()}")
print(f"Random Double: {bitgen.random_double()}")

print(f"Random Binomial: {gen.binomial(4, 1/4)}")
print(f"Random Exponential: {gen.exponential()}")
print(f"Random Logistic: {gen.logistic()}")
print(f"Random Poisson: {gen.poisson()}")
print(f"Random Std. Normal: {gen.standard_normal()}")
print(f"Random Triangular: {gen.triangular(-1, 0, 1)}")
# ...
```


# Documentation

## QiskitBitGenerator
A quantum random bit-generator based on Qiskit, which can interface with NumPy's random module (e.g. to instantiate Generator objects). It implements an efficient strategy to retrieve random bits from IBMQ's quantum backends.

On each request to a backend, it retrieves as many bits as possible and stores them in a cache. This way, the number of internet connections leading to overheads is greatly reduced and, while the cache is loaded, random bits can be retrieved "instantaneously". The user can limit the number of bits to retrieve on each request through the `max_bits_per_request` argument.

Additionally, it always chooses the least busy backend from the list of available machines. This list can be filtered by the user through the `backend_filter` argument, which defaults to history-enabled non-simulators. If a Qiskit Backend is explicitly passed in as argument, no backend selection will be performed: effectively ignoring any Qiskit Provider object passed. If neither `provider` nor `backend` are passed as inputs, it will default to running Qiskit BasicAer's 'qasm_simulator' locally.

### ARGUMENTS
- **provider**: *Optional[Provider] = None* <br/>
  A Qiskit Provider object to access quantum backends. If `None` it defaults to BasicAer.
- **backend**: *Optional[Backend] = None* <br/>
  A Qiskit Backend object to produce random bits. If not `None`, `provider` will be ignored.
- **backend_filter**: *Optional[BackendFilter] = None* <br/>
  A Callable that takes in a Qiskit Backend object and returns `True` if it meets certain requirements, `False` otherwise. This is used to filter the list of available backends from which to dynamically choose on each request to the `provider` (if no `backend` is explicitly input). If `None` it defaults to `QiskitBitGenerator.default_backend_filter`.
- **max_bits_per_request**: *int = 0* <br/>
  A limit to the number of bits to be retrieved on each request to any Qiskit Backend. If less than one, no bound will be applied and the maximum allowed number of bits will be retrieved.
- **ISRAW32**: *Final[bool] = False* <br/>
  Toggle 32-bit BitGenerator mode. If `False` the BitGenerator will be 64-bit. This determines the number of bits returned by NumPy's `random_raw()` method, and the default number of bits to output on `random_uint()` and `random_double()`. Once an object is instantiated, this cannot be overridden.

### STATIC / CLASS METHODS
- **default_backend_filter** *(b: Backend) -> bool*: <br/>
  Default backend filter. A Callable that takes in a Qiskit Backend object and returns `True` if it is not a simulator and has memory enabled, `False` otherwise.
- **get_best_backend** *(cls, provider: Provider, backend_filter: Optional[BackendFilter] = None) -> Backend*: <br/>
  Returns the least busy backend available to an input provider, and according to certain filter(s).
  - ARGUMENTS
    - *provider*: Provider <br/>
      A Qiskit Provider object to access quantum backends.
    - *backend_filter*: Optional[BackendFilter] = None <br/>
      A Callable that takes in a Qiskit Backend object and returns `True` if it meets certain requirements, `False` otherwise. If `None` it defaults to `cls.default_backend_filter`.
  - RETURNS
    - *out*: Backend <br/>
      Least busy backend from the filtered list of available backends.

### PUBLIC METHODS
- **dump_cache** *(self, flush: bool = False) -> str*: <br/>
  Returns all the contents stored in the cache.
  - ARGUMENTS
    - *flush*: bool <br/>
      If `True` erase the cache after dumping.
  - RETURNS
    - *out*: str <br/>
      The bitstring stored in cache.
- **flush_cache** *(self) -> bool*: <br/>
  Erase the cache.
  - RETURNS
    - *out*: bool <br/>
      `True` if succeeds, `False` otherwise.
- **random_bitstring** *(self, n_bits: int = 0) -> str*: <br/>
  Returns a random bitstring of a given lenght.
  - ARGUMENTS
    - *n_bits*: int <br/>
      Number of bits to retrieve. If less than one it defaults to the raw number of bits for the instance QiskitBitGenerator (i.e. 32 or 64).
  - RETURNS
    - *out*: str <br/>
      Bitstring of lenght `n_bits`.
- **random_double** *(self, n: float = 1) -> float*: <br/>
  Returns a random double from a uniform distribution in the range [0,n). Defaults to [0,1).
  - ARGUMENTS
    - *n*: float <br/>
      Size of the range [0,n) from which to draw the random number.
  - RETURNS
    - *out*: float <br/>
      Random float in the range [0,n).
- **random_raw** *(self) -> int*: <br/>
  Returns a random unsigned int of either 32 or 64 bits.
  - RETURNS
    - *out*: int <br/>
      Unsigned int of either 32 or 64 bits.
- **random_uint** *(self, n_bits: int = 0) -> int*: <br/>
  Returns a random unsigned int of a given size in bits.
  - ARGUMENTS
    - *n_bits*: int <br/>
      Number of bits to retrieve. If less than one it defaults to the raw number of bits for the instance QiskitBitGenerator (i.e. 32 or 64).
  - RETURNS
    - *out*: int <br/>
      Unsigned int of `n_bits` bits.
- **load_cache** *(self, bitstring: str, flush: bool = False) -> bool*: <br/>
  Load cache contents from bitstring.
  - ARGUMENTS
    - *bitstring*: str <br/>
      The bitstring to load to cache.
    - *flush*: bool <br/>
      If `True` erase cache before loading.
  - RETURNS
    - *out*: bool <br/>
      `True` if succeeds, `False` otherwise.
  - RAISES
    - *TypeError* <br/>
      If input bitstring is not str
    - *ValueError* <br/>
      If input bitstring is not a valid bitstring
- **set_state** *(self, provider: Optional[Provider] = None, backend: Optional[Backend] = None, backend_filter: Optional[BackendFilter] = None, max_bits_per_request: Optional[int] = None) -> bool*: <br/>
  Override constructor arguments. Any change must be explicitly passed as input (i.e. not `None`).
  - ARGUMENTS
    - *provider*: Optional[Provider] = None <br/>
      Same as constructor.
    - *backend*: Optional[Backend] = None <br/>
      Same as constructor.
    - *backend_filter*: Optional[BackendFilter] = None <br/>
      Same as constructor.
    - *max_bits_per_request*: Optional[int] = None <br/>
      Same as constructor.
  - RETURNS
    - *out*: bool <br/>
      `True` if any changes were made, `False` otherwise.

### PUBLIC PROPERTIES
- **bits**: *Final[int]* <br/>
  The number of bits output by NumPy's `random_raw()` method. Either 32 or 64.
- **state**: *dict* <br/>
  Parsed information about the current state of the QiskitBitGenerator.


# Acknowledgements

Parts of this software's source code have been borrowed from the [qRNG](https://github.com/ozanerhansha/qRNG) project, which is licensed under the [GNU GPLv3](https://github.com/ozanerhansha/qRNG/blob/master/LICENSE) license. Copyright notice and specific changes can be found as a docstring wherever this applies.

---
(c) Copyright 2020 Pedro Rivero
