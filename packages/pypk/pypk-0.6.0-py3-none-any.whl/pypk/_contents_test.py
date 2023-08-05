from . import _contents


def test_pyproject():
    expected = """[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"

[tool.black]
line-length = 120
target-version = ["py36"]

[tool.isort]
profile = "black"
"""
    actual = _contents.PYPROJECT.format(package_name="foo", target_version="py36")
    assert actual == expected


def test_readme():
    expected = """# foo
"""
    actual = _contents.README.format(package_name="foo")
    assert actual == expected


def test_setup():
    expected = """from pathlib import Path

from setuptools import find_packages, setup

HERE = Path(__file__).parent
README = HERE.joinpath("README.md").read_text()
REQUIREMENTS = HERE.joinpath("requirements", "requirements.in").read_text().split()

setup(
    name="foo",
    author="bar",
    author_email="baz@cool.com",
    description="hi there",
    long_description=README,
    long_description_content_type="text/markdown",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=REQUIREMENTS,
    python_requires=">=3.6.0",
)
"""
    actual = _contents.SETUP.format(
        package_name="foo", author="bar", author_email="baz@cool.com", description="hi there", python_version="3.6.0"
    )
    assert actual == expected


def test_precommit():
    expected = """# See https://pre-commit.com for more information
# See https://pre-commit.com/hooks.html for more hooks
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.1.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-json
      - id: check-yaml
      - id: check-added-large-files
  - repo: https://github.com/PyCQA/isort
    rev: 5.10.1
    hooks:
      - id: isort
  - repo: https://github.com/psf/black
    rev: 22.1.0
    hooks:
      - id: black
        language_version: python3
  - repo: https://gitlab.com/pycqa/flake8
    rev: 4.0.1
    hooks:
      - id: flake8
        additional_dependencies: [flake8-bugbear]
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.1
    hooks:
      - id: bandit
        args: ["-x", "*/**/*_test.py"]
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest src/foo
        language: system
        pass_filenames: false
        types: [python]
"""
    actual = _contents.PRECOMMIT.format(package_name="foo")
    assert actual == expected
