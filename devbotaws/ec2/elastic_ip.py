from . import utils


def allocate_elastic_ip(connection):
    return connection.allocate_address()


def release_elastic_ip(connection, ip_address):
    return connection.release_address(ip_address)


def allocate_elastic_ip_with_conf(connection, conf):
    conf_data = conf['elastic_ips']

    # we will replace the existing conf['elastic_ips']
    # with fully allocated ips if need be.
    data = {}

    for key, value in utils.process_group(conf_data):
        if value is None:
            addy = allocate_elastic_ip(connection)
            data[key] = addy.public_ip
        else:
            data[key] = value

    conf['elastic_ips'] = data

