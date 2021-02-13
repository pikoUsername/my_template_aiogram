from pathlib import Path
import pytoml


def load_config(path: Path):
    with open(path / "data" / "app.toml") as f:
        d = pytoml.load(f)
    return d
