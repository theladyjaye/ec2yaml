import yaml


def load_config(path):
    data = None

    with open(path) as f:
        data = yaml.load(f.read())

    return data
