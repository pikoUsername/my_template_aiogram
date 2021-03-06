from pathlib import Path
import pytoml

__all__ = "load_config",


def load_config(path: Path) -> dict:
    # loads a config, and pytoml.load func parses to dict
    with open(path / "data" / "app.toml") as f:
        d = pytoml.load(f)
    # returns dict
    return d
