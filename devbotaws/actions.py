from devbotaws.ec2 import config
from devbotaws.ec2.instances import instances_with_conf
from devbotaws.ec2.utils import connection_from_config

from devbotaws.ec2.elastic_ip import (
    allocate_elastic_ip_with_conf, assign_ips_with_conf
)

from devbotaws.ec2.security_groups import (
    security_groups_with_conf, create_application_security_group
)


def initialize_with_conf(path):
    conf = config.config_with_path(path)
    conn = connection_from_config(conf)

    allocate_elastic_ip_with_conf(conn, conf)
    security_groups_with_conf(conn, conf)
    create_application_security_group(conn, conf['app']['name'])

    for key, value in conf['instances'].iteritems():
        value['security_groups'].append(conf['app']['name'])

    instances_with_conf(conn, conf)
    assign_ips_with_conf(conf)
