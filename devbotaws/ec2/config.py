import yaml
from .errors import InvalidConfig


def load_config(path):
    data = None

    with open(path) as f:
        data = yaml.load(f.read())

    validate_config(data)
    return data


def validate_config(config):

    if 'app' not in config:
        raise InvalidConfig('Missing \'app\' key')

    if 'name' not in config['app'] or config['app']['name'] is None:
        raise InvalidConfig('\'app\' must contain a \'name\' value')

    if 'owner' not in config['app'] or config['app']['owner'] is None:
        raise InvalidConfig('\'app\' must contain an \'owner\' value')

