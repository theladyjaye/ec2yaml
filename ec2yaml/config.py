import logging
import yaml
from .errors import InvalidConfig

log = logging.getLogger(__name__)


def config_with_string(data):
    return yaml.load(data)


def config_with_path(path):
    global log
    data = None

    log.debug('Loading config at path \'%s\'', path)

    with open(path) as f:
        data = config_with_string(f.read())

    validate_config(data)
    return data


def validate_config(config):

    if 'app' not in config:
        raise InvalidConfig('Missing \'app\' key')

    if 'name' not in config['app'] or config['app']['name'] is None:
        raise InvalidConfig('\'app\' must contain a \'name\' value')

    if 'owner' not in config['app'] or config['app']['owner'] is None:
        raise InvalidConfig('\'app\' must contain an \'owner\' value')
