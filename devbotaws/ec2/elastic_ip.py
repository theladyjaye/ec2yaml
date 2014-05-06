import logging
import re
from . import utils

log = logging.getLogger(__name__)


def allocate_elastic_ip(connection):
    log.debug('Allocating elastic IP')
    return connection.allocate_address()


def release_elastic_ip(connection, ip_address):
    return connection.release_address(ip_address)


def assign_ip(instance, ip_address):
    instance.use_ip(ip_address)


def assign_ips_with_conf(conf):
    global log

    log.info('Assigning elastic IPs to instances')

    try:
        ips = conf['elastic_ips']
    except KeyError:
        log.debug('No elastic IPs to assign')
        return

    instances = conf['instances']

    is_ip_address = re.compile(
        r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}'
        r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b')

    for key, value in instances.iteritems():
        candidate = value.get('ip_address', None)
        if not candidate:
            continue

        if is_ip_address.match(candidate):
            assign_ip(value['instance'], candidate)
        else:
            candidate = ips.get(candidate)
            assign_ip(value['instance'], candidate)


def allocate_elastic_ip_with_conf(connection, conf):
    global log

    log.info('Initializing elastic IPs')

    try:
        conf_data = conf['elastic_ips']
    except KeyError:
        log.debug('No elastic IPs to initialize')
        return

    # we will replace the existing conf['elastic_ips']
    # with fully allocated ips if need be.
    data = {}

    for key, value in utils.process_group(conf_data).iteritems():
        if value is None:
            addy = allocate_elastic_ip(connection)
            data[key] = addy.public_ip
        else:
            data[key] = value

    log.debug('Allocated the following Elastic IPs %s', data)
    conf['elastic_ips'] = data

