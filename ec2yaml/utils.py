import logging
import boto.ec2


log = logging.getLogger(__name__)
__CONNECTION__ = None


def connection(
        location='us-west-2',
        aws_access_key_id=None,
        aws_secret_access_key=None,
        profile_name=None):

    global __CONNECTION__

    if __CONNECTION__ is None:
        log.debug('Initializing connection for \'%s\'', location)
        if aws_access_key_id and aws_secret_access_key:
            log.debug('Using provided \'aws_access_key_id\''
                      ' and \'aws_secret_access_key\'.'
                      '\nNot loading from environment variables.')
        elif profile_name:
            log.debug('Using provided \'profile_name\''
                      '\nLoading from boto profile specified by boto-profile.')
        else:
            log.debug('Using provided \'AWS_ACCESS_KEY_ID\''
                      ' and \'AWS_SECRET_ACCESS_KEY\''
                      ' environment variables.')

        __CONNECTION__ = boto.ec2.connect_to_region(
            location,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            profile_name=profile_name
        )

    return __CONNECTION__


def connection_from_config(conf):
    location = conf['app'].get('location', 'us-east-1')
    key = conf['app'].get('key', None)
    secret = conf['app'].get('secret', None)
    boto_profile = conf['app'].get('boto_profile', None)

    return connection(
        location=location,
        aws_access_key_id=key,
        aws_secret_access_key=secret,
        profile_name=boto_profile)


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
