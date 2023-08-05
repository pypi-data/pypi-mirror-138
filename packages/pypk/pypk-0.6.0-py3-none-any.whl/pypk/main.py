import json
import sys
from pathlib import Path
from typing import NoReturn, Optional

import typer

from . import core
from .config import load_custom_config, save_as_default_config, try_load_default_config
from .version import version as pypk_version

_CURRENT_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}.0"

app = typer.Typer()


def exit_with_status(msg: str, code: int = 1) -> NoReturn:
    typer.echo(msg, err=True)
    sys.exit(code)


@app.command()
def create(
    package: Path = typer.Argument(..., help="Path to root package directory"),  # noqa: B008
    config: Path = typer.Option(None, "--config", "-c", help="Path to config file"),  # noqa: B008
    author: str = typer.Option(None, "--author", "-a", help="Author's name"),  # noqa: B008
    email: str = typer.Option(None, "--email", "-e", help="Author's email"),  # noqa: B008
    description: Optional[str] = typer.Option(  # noqa: B008
        None, "--description", "-d", help="Description to be placed in setup.py"
    ),
    python_version: str = typer.Option(  # noqa: B008
        _CURRENT_VERSION, "--py-version", "-p", help="Minimum Python version supported"
    ),
    init_git: bool = typer.Option(None, "--init-git/--skip-git-init", help="Toggle Git initialization"),  # noqa: B008
    tests_dir: bool = typer.Option(  # noqa: B008
        None, "--create-tests-dir/--skip-tests-dir", help="Create a top-level tests directory"
    ),
) -> None:
    try:
        if config is not None:
            cfg = load_custom_config(config)
        else:
            cfg = try_load_default_config()
    except Exception as e:
        exit_with_status(f"[Error] failed to load config: '{e}'")

    author = author if author else cfg.get("author")
    email = email if email else cfg.get("email")
    python_version = python_version if python_version else cfg.get("py_version")
    init_git = init_git if init_git is not None else cfg.get("init_git", False)
    tests_dir = tests_dir if tests_dir is not None else cfg.get("tests_dir", False)

    if author is None:
        exit_with_status("[Error] 'author' must be specified in either the config or via command line")
    if email is None:
        exit_with_status("[Error] 'email' must be specified in either the config or via command line")
    if version is None:
        exit_with_status("[Error] 'version' must be specified in either the config or via command line")
    if not isinstance(init_git, bool):
        exit_with_status("[Error] 'init_git' must be a boolean")
    if not isinstance(tests_dir, bool):
        exit_with_status("[Error] 'tests_dir' must be a boolean")

    core.create(package, author, email, python_version, description=description, init_git=init_git, tests_dir=tests_dir)


@app.command()
def config(key: str, value: Optional[str] = typer.Argument(None)):  # noqa: B008
    try:
        cfg = try_load_default_config()
    except Exception as e:
        exit_with_status(f"[Error] failed to load config: '{e}'")

    if key not in ["author", "email", "py_version", "init_git", "tests_dir"]:
        exit_with_status(f"[Error] invalid key '{key}'")

    if value:
        if key in ["init_git", "tests_dir"]:
            value = json.loads(value.lower())  # hacky, but it works
            if not isinstance(value, bool):
                exit_with_status(f"[Error] '{key}' must be a boolean")
        cfg[key] = value
        save_as_default_config(cfg)
    else:
        value = cfg.get(key)
        if value:
            typer.echo(f"'{key}' = '{value}'")
        else:
            typer.echo(f"'{key}' is not set")


@app.command()
def version():
    typer.echo(pypk_version)


__all__ = ["app"]
