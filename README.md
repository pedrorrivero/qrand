[![Unitary Fund](https://img.shields.io/badge/Supported_By-UNITARY_FUND-FFF000.svg?style=flat)](http://unitary.fund)
[![YouTube](https://img.shields.io/badge/PR-qrand-FF0000.svg?style=flat&logo=YouTube&logoColor=white)](https://youtu.be/CG7BxuWFpME)
[![PyPI](https://img.shields.io/pypi/v/qrand?label=PyPI&style=flat&color=3776AB&logo=Python&logoColor=white)](https://pypi.org/project/qrand/)
[![Coverage](https://img.shields.io/badge/Coverage-67%25-green.svg?style=flat)](http://pytest.org)
[![Apache-2.0 License](https://img.shields.io/github/license/pedrorrivero/qrand?label=License&style=flat&color=1D1D1D)](https://github.com/pedrorrivero/qrand/blob/master/LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4755731.svg)](https://doi.org/10.5281/zenodo.4755731)


# qrand

> A multiprotocol and multiplatform quantum random number generation framework

Random numbers are everywhere.

Computer algorithms, data encryption, physical simulations, and even the arts use them all the time. There is one problem though: it turns out that they are actually very difficult to produce in large amounts. Classical computers can only implement mathematical tricks to emulate randomness, while measuring it out of physical processes turns out to be too slow. Luckily, the probabilistic nature of quantum computers makes these devices particularly useful for the task.

QRAND is a free and open-source framework for quantum random number generation. Thanks to its loosely coupled design, it offers seamlessly compatibility between different [quantum computing platforms](#supported-quantum-platforms) and [QRNG protocols](#implemented-qrng-protocols). Not only that, but it also enables the creation of custom cross-compatible protocols, and a wide range of output formats (e.g. bitstring, int, float, complex, hex, base64).

To boost its efficiency, QRAND makes use of a concurrent cache to reduce the number of internet connections needed for random number generation; and for quality checks, it incorporates a suite of classical entropy validation tests which can be easily plugged into any base protocol.

Additionally, QRAND introduces an interface layer for [NumPy](https://numpy.org/) that enables the efficient production of quantum random numbers (QRN) adhering to a wide variety of probability distributions. This is ultimately accomplished by transforming uniform probability distributions produced in cloud-based real quantum hardware, through NumPy's random module.

```python3
from qrand import QuantumBitGenerator
from qrand.platforms import QiskitPlatform
from qrand.protocols import HadamardProtocol
from numpy.random import Generator
from qiskit import IBMQ

provider = IBMQ.load_account()
platform = QiskitPlatform(provider)
protocol = HadamardProtocol()
bitgen = QuantumBitGenerator(platform, protocol)
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

## Supported quantum platforms
As of May 2021, only [`Qiskit`](https://qiskit.org/) is supported. However, support for [`Cirq`](https://quantumai.google/cirq) and [`Q#`](https://docs.microsoft.com/en-us/azure/quantum/user-guide/?view=qsharp-preview) is under active development.

## Implemented QRNG protocols
As of May 2021, only the basic `HadamardProtocol` is available. We are also working on implementing this [`EntaglementProtocol`](https://www.nature.com/articles/s41598-019-56706-2), as well as a version of [Google's Sycamore routine](https://arxiv.org/abs/1612.05903) (patent permitting).

## Authors and citation
QRAND is the work of many people who contribute to the project at
different levels. If you use QRAND, please cite as per the included
[BibTeX file](QRAND.bib).

<!-- ## Documentation -->

## Contribution guidelines
If you'd like to contribute to QRAND, please take a look at the
[contribution guidelines](CONTRIBUTING.md). This project adheres to the following [code of conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

We use [GitHub issues](https://github.com/pedrorrivero/qrand/issues) for tracking requests and bugs. Please use Unitary Fund's [Discord](http://discord.unitary.fund/) for discussion and simple questions.

## Acknowledgements
Parts of this software's source code have been borrowed from the [qRNG](https://github.com/ozanerhansha/qRNG) project, which is licensed under the [GNU GPLv3](https://github.com/ozanerhansha/qRNG/blob/master/LICENSE) license. Copyright notice and specific changes can be found as a docstring wherever this applies.

## License
[Apache License 2.0](LICENSE)

---
(c) Copyright 2021 Pedro Rivero
