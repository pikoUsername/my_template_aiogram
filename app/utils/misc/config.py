import pytoml


def load_config(path) -> dict:
    # loads a config, and pytoml.load func parses to dict
    with open(path / "data" / "app.toml") as f:
        d = pytoml.load(f)
    # returns dict
    return d
