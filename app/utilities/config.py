import os
import yaml

def load_config(path="config.yaml"):
    with open(path, "r") as f:
        raw = yaml.safe_load(f)

    # Expand user (~) and normalize paths
    raw["folders"] = [os.path.expanduser(p) for p in raw.get("folders", [])]
    raw["skip_exts"] = tuple(ext.lower() for ext in raw.get("skip_exts", []))
    return raw
