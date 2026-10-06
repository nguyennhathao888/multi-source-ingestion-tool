import yaml

def load_soucre(path: str="source.yaml"):
    with open(path, "r",encoding="utf-8") as f:
        config=yaml.safe_load(f)
    return config["source"]

