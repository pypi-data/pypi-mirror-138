# pypk

An opinionated Python packaging template generator.

## Overview

pypk autogenerates a complete python package skeleton that is installable out of the box. It assumes the following tools
are used in your development workflow:

- pip
- [pip-tools](https://github.com/jazzband/pip-tools)
- [bandit](https://github.com/PyCQA/bandit)
- [black](https://github.com/psf/black)
- [flake8](https://github.com/pycqa/flake8)/[flake8-bugbear](https://github.com/PyCQA/flake8-bugbear)
- [isort](https://github.com/PyCQA/isort)
- [pre-commit](https://github.com/pre-commit/pre-commit)
- [pytest](https://github.com/pytest-dev/pytest)
- [safety](https://github.com/pyupio/safety)


However, once the template is generated, pypk gets out of your way, so you are free to add and/or remove tools,
frameworks, and libraries as needed.

## Installation

`pip install pypk`

## Getting Started

It's recommended you install and use pypk in the same virtual environment you plan to develop your Python package in.

### Project Creation

To create a new skeleton project, run the `create` command:

```sh
pypk create </path/to/project/root> -a <author-name> -e <author-email>
```

Additionally, you can pass the following arguments:

- `-c/--config`: a json config file (see the [Configuration](#configuration) section).
- `-d/--description`: set the package description in the generated `setup.py`
- `-p/--py-version`: set the minimum Python version supported by the project.
- `--init-git/--skip-git-init`: initialize git in the generated project (or skip it).
- `--create-tests-dir/--skip-tests-dir`: create a top level tests directory in the generated project (or skip it).

Run `pypk create --help` for more details.

### Configuration

pypk supports a configuration which holds (default) parameters for project creation. Specifically, the following
parameters can be set in a json config file:

- `author` (key=`author`)
- `email` (key=`email`)
- `description` (key=`description`)
- `py-version` (key=`py_version`)
- `init-git` (key=`init_git`)
- `create-tests-dir` (key=`tests_dir`)

Additionally, default values can be set via the cli so they do not need to be specified whenver the `create` command is
run. pypk will create a json file under the `user config dir` as defined by [appdirs](https://github.com/ActiveState/appdirs).
To set a value, run the following:

```sh
pypk config <key> <value>
```

To print out the currently set value, run:

```sh
pypk config <key>
```

## License

MIT
