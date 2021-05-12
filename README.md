[![Unitary Fund](https://img.shields.io/badge/Supported_By-UNITARY_FUND-FFF000.svg?style=flat)](http://unitary.fund)
[![YouTube](https://img.shields.io/badge/PR-qrand-FF0000.svg?style=flat&logo=YouTube&logoColor=white)](https://youtu.be/CG7BxuWFpME)
[![PyPI](https://img.shields.io/pypi/v/qrand?label=PyPI&style=flat&color=3776AB&logo=Python&logoColor=white)](https://pypi.org/project/qrand/)
[![Coverage](https://img.shields.io/badge/Coverage-97%25-green.svg?style=flat)](http://pytest.org)
[![Apache-2.0 License](https://img.shields.io/github/license/pedrorrivero/qrand?label=License&style=flat&color=1D1D1D)](https://github.com/pedrorrivero/qrand/blob/master/LICENSE)


# qrand

> A multiprotocol and multiplatform quantum random number generation FOSS framework

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

## Authors and Citation
QRAND is the work of many people who contribute to the project at
different levels. If you use QRAND, please cite as per the included
[BibTeX file](QRAND.bib).

<!-- ## Documentation -->

## Contribution Guidelines
If you'd like to contribute to QRAND, please take a look at the
[contribution guidelines](CONTRIBUTING.md). This project adheres to QRAND's [code of conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

We use [GitHub issues](https://github.com/pedrorrivero/qrand/issues) for tracking requests and bugs. Please use Unitary Fund's [Discord](http://discord.unitary.fund/) for discussion and simple questions.

## Acknowledgements
Parts of this software's source code have been borrowed from the [qRNG](https://github.com/ozanerhansha/qRNG) project, which is licensed under the [GNU GPLv3](https://github.com/ozanerhansha/qRNG/blob/master/LICENSE) license. Copyright notice and specific changes can be found as a docstring wherever this applies.

## License
[Apache License 2.0](LICENSE)

---
(c) Copyright 2021 Pedro Rivero
