[![code style: black](https://img.shields.io/badge/Code_Style-black-000000.svg?style=flat)](https://github.com/psf/black)
[![docs style: NumPy](https://img.shields.io/badge/Docs_Style-NumPy-013243.svg?style=flat&logo=NumPy&logoColor=white)](https://numpydoc.readthedocs.io/en/latest/format.html)
[![commit style: Conventional Commits](https://img.shields.io/badge/Commit_Style-Conventional_Commits-E86F76.svg?style=flat)](https://www.conventionalcommits.org/)

[![Poetry](https://img.shields.io/badge/Poetry-3B8BD8.svg?style=flat)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-FAB040.svg?style=flat&logo=pre-commit&logoColor=white)](https://pre-commit.com/)

# Contributing
## Install
To contribute to this project you will need to install [poetry](https://python-poetry.org/docs/#installation), fork this repo, and clone your copy locally. Then run:

```sh
$ poetry install  # Install dependencies
Using python3 (3.8.2)
Creating virtualenv qrand in ./.venv
Installing dependencies from lock file

Package operations: 11 installs, 0 updates, 0 removals

  • Installing appdirs (1.4.4)
  • Installing distlib (0.3.1)
  • Installing filelock (3.0.12)
  • Installing six (1.15.0)
  • Installing cfgv (3.2.0)
  • Installing identify (1.5.6)
  • Installing nodeenv (1.5.0)
  • Installing pyyaml (5.3.1)
  • Installing toml (0.10.1)
  • Installing virtualenv (20.0.34)
  • Installing pre-commit (2.7.1)

Installing the current project: qrand (0.0.0)
```

The resulting virtual environment with all the dependencies is activated as usual. If located [inside the repo](https://python-poetry.org/docs/configuration/#virtualenvsin-project-boolean) (i.e. `poetry config virtualenvs.in-project true` before `poetry install`):

```sh
$ source .venv/bin/activate
```

Alternatively this [one-liner](https://python-poetry.org/docs/basic-usage/#activating-the-virtual-environment) is available:

```sh
source `poetry env info --path`/bin/activate
```

Finally, git hooks are available via:

```sh
(.venv) $ pre-commit install  # Install pre-commit hooks
pre-commit installed at .git/hooks/pre-commit
(.venv) $ pre-commit install --hook-type commit-msg # Install commit-msg hooks
pre-commit installed at .git/hooks/commit-msg
```

## Documentation
For this project we adhere to the [numpydoc docstring guide](https://numpydoc.readthedocs.io/en/latest/format.html). If you make any changes to the code, remember updating the docstring wherever relevant.


# Known issues
## MacOS (10-13-2020)
[As of October 2020](https://github.com/ycm-core/YouCompleteMe/issues/3770), MacOS Xcode ships with python 3.8.2 specially set up to support future arm64 architectures. This will cause the build process of `regex` (a dependency of `black`) to fail, which in turn will cause an error when the pre-commit hooks get executed for the first time (i.e. on `git commit`). To fix this issue one must create the virtual environment with a compatible version of python before running `poetry install` (e.g. using [homebrew](https://brew.sh/)):

```sh
$ brew install python@3.9
$ virtualenv .venv -p /usr/local/Cellar/python@3.9/3.9.0/bin/python3.9
```

This requires `virtualenv` to be installed beforehand.

---
(c) 2021 Pedro Rivero
