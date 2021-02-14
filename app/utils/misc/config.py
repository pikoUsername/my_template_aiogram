from pathlib import Path
import pytoml

__all__ = ("load_config",)

def load_config(path: Path):
    with open(path / "data" / "app.toml") as f:
        d = pytoml.load(f)
    return d
