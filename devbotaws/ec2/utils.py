import logging
import boto.ec2


log = logging.getLogger(__name__)
__CONNECTION__ = None


def connection(location='us-west-2'):
    global __CONNECTION__

    if __CONNECTION__ is None:
        log.debug('Initializing connection for \'%s\'', location)
        __CONNECTION__ = boto.ec2.connect_to_region(location)

    return __CONNECTION__


def connection_from_config(conf):
    location = conf['app'].get('location', 'us-east-1')
    return connection(location=location)


def key_for_group(item):
    # basestring only works in python 2
    if isinstance(item, basestring):
        return item

    if isinstance(item, dict):
        return item.keys()[0]


def value_for_group(item):
    # basestring only works in python 2
    if isinstance(item, basestring):
        return None

    if isinstance(item, dict):
        return item.values()[0]


def process_group(items):
    data = {}
    for each in items:
        key = key_for_group(each)
        value = value_for_group(each)
        data[key] = value

    return data
