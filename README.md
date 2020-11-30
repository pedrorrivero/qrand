[![Unitary Fund](https://img.shields.io/badge/Supported_By-UNITARY_FUND-FFF000.svg?style=flat)](http://unitary.fund)
[![YouTube](https://img.shields.io/badge/PR-qrand-FF0000.svg?style=flat&logo=YouTube&logoColor=white)](https://youtu.be/CG7BxuWFpME)
[![PyPI](https://img.shields.io/pypi/v/qrand?label=PyPI&style=flat&color=3776AB&logo=Python&logoColor=white)](https://pypi.org/project/qrand/)
[![MIT License](https://img.shields.io/github/license/pedrorrivero/qrand?label=License&style=flat&color=1D1D1D)](https://github.com/pedrorrivero/qrand/blob/master/LICENSE)


# qrand

> A quantum random number generator for arbitrary probability distributions

Random numbers are everywhere.

Computer algorithms, data encryption, physical simulations, and even the arts use them all the time. There is one problem though: it turns out that they are actually very difficult to produce in large amounts. Classical computers can only implement mathematical tricks to emulate randomness, while measuring it out of physical processes turns out to be too slow.

Luckily, the probabilistic nature of quantum computers makes these devices particularly useful for the task. Nonetheless, most of the current efforts in producing quantum random numbers have been focused on uniform probability distributions. Despite this fact, many applications actually need to sample from more complex distributions (e.g. gaussian, poisson).

This is why I am setting up to develop an easy to use, modular piece of software, capable of producing quantum random numbers from arbitrary distributions. To do so, I will be using mathematical processing alongside IBM's Qiskit framework.


# Documentation

## QiskitBitGenerator
Quantum random bit-generator based on Qiskit, which can interface with NumPy's random library (e.g. to instantiate Generator objects). It implements an efficient strategy to retrieve random bits from IBMQ quantum backends.

On each request to a backend, it retrieves as many bits as possible and stores them in a cache. This way, the number of internet connections leading to overheads is greatly reduced and, while the cache is loaded, random bits can be retrieved "instantaneously". The user can limit the number of bits to retrieve on each request through the `max_bits_per_request` argument.

Additionally, it always chooses the least busy backend from the list of available machines. This list can be filtered by the user through the `backend_filter` argument, which defaults to history-enabled non-simulators. If a Qiskit Backend is explicitly passed in as argument, no backend selection will be performed: effectively ignoring any Qiskit Provider object passed. If neither `provider` nor `backend` are passed as inputs, it will default to running Qiskit BasicAer's 'qasm_simulator' locally.

### ARGUMENTS
- **provider**: *Optional[Provider] = None*
  A Qiskit Provider object to access quantum backends. If `None` it defaults to BasicAer.
- **backend**: *Optional[Backend] = None*
  A Qiskit Backend object to produce random bits. If not `None`, `provider` will be ignored.
- **backend_filter**: *Optional[BackendFilter] = None*
  A Callable that takes in a Qiskit Backend object and returns `True` if it meets certain requirements, `False` otherwise. This is used to filter the list of available backends from which to dynamically choose on each request to the `provider` (if no `backend` is explicitly input). If `None` it defaults to `QiskitBitGenerator.default_backend_filter`.
- **max_bits_per_request**: *int = 0*
  A limit to the number of bits to be retrieved on each request to any Qiskit Backend. If less than one, no bound will be applied and the maximum allowed number of bits will be retrieved.
- **ISRAW32**: *Final[bool] = False*
  Toggle 32-bit BitGenerator mode. If `False` the BitGenerator will be 64-bit. This determines the number of bits returned by NumPy's `random_raw()` method, and the default number of bits to output on `random_uint()` and `random_double()`. Once an object is instantiated, this cannot be overridden.

### STATIC / CLASS METHODS
- **default_backend_filter** *(b: Backend) -> bool*:
  Default backend filter. A Callable that takes in a Qiskit Backend object and returns `True` if it is not a simulator and has memory enabled, `False` otherwise.
- **get_best_backend** *(cls, provider: Provider, backend_filter: Optional[BackendFilter] = None) -> Backend*:
  Returns the least busy backend available to an input provider, and according to certain filter(s).
  - ARGUMENTS
    *provider*: Provider
      A Qiskit Provider object to access quantum backends.
    *backend_filter*: Optional[BackendFilter] = None
      A Callable that takes in a Qiskit Backend object and returns `True` if it meets certain requirements, `False` otherwise. If `None` it defaults to `cls.default_backend_filter`.
  - RETURNS
    *out*: Backend
      Least busy backend from the filtered list of available backends.

### PUBLIC METHODS
- **dump_cache** *(self, flush: bool = False) -> str*:
  Returns all the contents stored in the cache.
  - ARGUMENTS
    *flush*: bool
      If `True` erase the cache after dumping.
  - RETURNS
    *out*: str
      The bitstring stored in cache.
- **flush_cache** *(self) -> bool*:
  Erase the cache.
  - RETURNS
    *out*: bool
      `True` if succeeds, `False` otherwise.
- **random_bitstring** *(self, n_bits: int = 0) -> str*:
  Returns a random bitstring of a given lenght.
  - ARGUMENTS
    *n_bits*: int
      Number of bits to retrieve. If less than one it defaults to the raw number of bits for the instance QiskitBitGenerator (i.e. 32 or 64).
  - RETURNS
    *out*: str
      Bitstring of lenght `n_bits`.
- **random_double** *(self, n: float = 1) -> float*:
  Returns a random double from a uniform distribution in the range [0,n). Defaults to [0,1).
  - ARGUMENTS
    *n*: float
      Size of the range [0,n) from which to draw the random number.
  - RETURNS
    *out*: float
      Random float in the range [0,n).
- **random_raw** *(self) -> int*:
  Returns a random unsigned int of either 32 or 64 bits.
  - RETURNS
    *out*: int
      Unsigned int of either 32 or 64 bits.
- **random_uint** *(self, n_bits: int = 0) -> int*:
  Returns a random unsigned int of a given size in bits.
  - ARGUMENTS
    *n_bits*: int
      Number of bits to retrieve. If less than one it defaults to the raw number of bits for the instance QiskitBitGenerator (i.e. 32 or 64).
  - RETURNS
    *out*: int
      Unsigned int of `n_bits` bits.
- **load_cache** *(self, bitstring: str, flush: bool = False) -> bool*:
  Load cache contents from bitstring.
  - ARGUMENTS
    *bitstring*: str
      The bitstring to load to cache.
    *flush*: bool
      If `True` erase cache before loading.
  - RETURNS
    *out*: bool
      `True` if succeeds, `False` otherwise.
- **set_state** *(self, provider: Optional[Provider] = None, backend: Optional[Backend] = None, backend_filter: Optional[BackendFilter] = None, max_bits_per_request: Optional[int] = None) -> bool*:
  Override constructor arguments. Any change must be explicitly passed as input (i.e. not `None`).
  - ARGUMENTS
    *provider*: Optional[Provider] = None
      Same as constructor.
    *backend*: Optional[Backend] = None
      Same as constructor.
    *backend_filter*: Optional[BackendFilter] = None
      Same as constructor.
    *max_bits_per_request*: Optional[int] = None
      Same as constructor.
  - RETURNS
    *out*: bool
      `True` if any changes were made, `False` otherwise.

### PUBLIC PROPERTIES
- **bits**: *int*
  The number of bits output by Numpy's `random_raw()` method. Either 32 or 64.
- **state**: *dict*
  Parsed information about the current state of the QiskitBitGenerator.


# Acknowledgements

Parts of this software's source code have been borrowed from the [qRNG](https://github.com/ozanerhansha/qRNG) project, which is licensed under the [GNU GPLv3](https://github.com/ozanerhansha/qRNG/blob/master/LICENSE) license. Copyright notice and specific changes can be found as a docstring wherever this applies.

---
(c) Copyright 2020 Pedro Rivero
