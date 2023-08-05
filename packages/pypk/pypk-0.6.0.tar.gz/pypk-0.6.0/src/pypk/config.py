import json
from pathlib import Path
from typing import Dict

from appdirs import user_config_dir


def load_custom_config(path: Path) -> Dict[str, str]:
    config = json.loads(path.read_text())
    if not isinstance(config, dict):
        raise ValueError("the config object must be a flat dictionary")
    return config


def try_load_default_config() -> Dict[str, str]:
    config_path = Path(user_config_dir("pypk", "Pyrite AI")).joinpath("config.json")
    try:
        config = json.loads(config_path.read_text())
    except FileNotFoundError:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with config_path.open("w") as f:
            json.dump({}, f)
        return {}
    except (OSError, json.decoder.JSONDecodeError):
        print("[Warning] failed to read default config file: invalid JSON")
        return {}
    else:
        return config


def save_as_default_config(cfg: Dict[str, str]):
    config_path = Path(user_config_dir("pypk", "Pyrite AI")).joinpath("config.json")
    with config_path.open("w") as f:
        json.dump(cfg, f)


__all__ = ["load_custom_config", "save_as_default_config", "try_load_default_config"]
