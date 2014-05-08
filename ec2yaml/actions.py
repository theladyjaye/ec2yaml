import logging
from . import config
from .instances import instances_with_conf
from .utils import connection_from_config

from .elastic_ip import (
    allocate_elastic_ip_with_conf, assign_ips_with_conf
)

from .volumes import (
    volumes_with_conf, assign_volumes_with_conf
)


from .security_groups import (
    security_groups_with_conf, create_application_security_group
)

log = logging.getLogger(__name__)


def coroutine(func):

    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        next(cr)
        return cr

    return start


@coroutine
def elastic_ips_processor(conn, conf):

    if 'elastic_ips' not in conf:
        return

    allocate_elastic_ip_with_conf(conn, conf)

    yield

    assign_ips_with_conf(conf)

    # prevent StopIteration
    yield


@coroutine
def volumes_processor(conn, conf):

    if 'volumes' not in conf:
        return

    volumes_with_conf(conn, conf)

    yield

    assign_volumes_with_conf(conf)

    # prevent StopIteration
    yield


def security_groups_processor(conn, conf):

    if 'security_groups' not in conf:
        return

    security_groups_with_conf(conn, conf)
    create_application_security_group(conn, conf['app']['name'])


def instances_processor(conn, conf):
    global log

    if 'instances' not in conf:
        return

    for key, value in conf['instances'].iteritems():
        security_groups = value.setdefault('security_groups', [])

        if len(security_groups) == 0:
            log.error('Unable to create instance \'{0}\'.'
                      'No security groups defined.')
            del conf['instances'][key]
            continue

        security_groups.append(conf['app']['name'])

    instances_with_conf(conn, conf)


def initialize_with_conf(conf):
    conn = connection_from_config(conf)
    elastic_ips = elastic_ips_processor(conn, conf)
    volumes = volumes_processor(conn, conf)
    security_groups_processor(conn, conf)
    instances_processor(conn, conf)

    # semantic var
    _next = None

    if 'elastic_ips' in conf and 'instances' in conf:
        elastic_ips.send(_next)

    if 'volumes' in conf and 'instances' in conf:
        volumes.send(_next)


def initialize_with_string(string):
    conf = config.config_with_string(string)
    initialize_with_conf(conf)


def initialize_with_path(path):
    conf = config.config_with_path(path)
    initialize_with_conf(conf)
