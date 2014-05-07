import logging


log = logging.getLogger(__name__)
GROUPS = None


def get_security_groups(connection, refresh=False):
    global GROUPS

    if GROUPS is None or refresh:
        GROUPS = connection.get_all_security_groups()
    return GROUPS


def get_security_group_names(connection, refresh=False):
    groups = get_security_groups(connection, refresh)
    return [x.name for x in groups]


def delete_security_group(connection, name):
    return connection.delete_security_group(name)


def create_security_group(connection, name, description=None):

    g = connection.create_security_group(name, description)
    _add_to_cached_groups(g)

    return g


def authorize_security_group(group, ip_protocol, from_port, to_port,
                             src_group=None, cidr_ip=None):

    global log
    log.info('Authorizing security group \'%s\'', group.name)
    kwargs = {
        'ip_protocol': ip_protocol,
        'from_port': from_port,
        'to_port': to_port,
    }

    if cidr_ip:
        kwargs['cidr_ip'] = cidr_ip

    if src_group:
        kwargs['src_group'] = src_group

    log.debug('Authorizing group \'%s\' with the following: %s',
              group.name, kwargs)

    group.authorize(**kwargs)


def deauthorize_security_group(group, ip_protocol, from_port, to_port,
                               src_group=None, cidr_ip=None):
    group.revoke(
        ip_protocol=ip_protocol,
        from_port=from_port,
        to_port=to_port,
        src_group=src_group,
        cidr_ip=cidr_ip)


def _add_to_cached_groups(group):
    global GROUPS

    if GROUPS is None:
        GROUPS = [group]
    else:
        GROUPS.append(group)


def create_application_security_group(connection, name, description=None):
    global log
    log.info('Initializing application security group \'%s\'', name)

    if name in get_security_group_names(connection):
        return

    group = connection.create_security_group(name, description)

    # allow all TCP communication intragroup
    authorize_security_group(
        group,
        ip_protocol='tcp',
        from_port=1,
        to_port=65535,
        src_group=group)

    # allow all icmp communication intragroup
    authorize_security_group(
        group,
        ip_protocol='icmp',
        from_port=-1,
        to_port=-1,
        src_group=group)

    # allow all udp communication intragroup
    authorize_security_group(
        group,
        ip_protocol='udp',
        from_port=1,
        to_port=65535,
        src_group=group)

    return group


def security_groups_with_conf(connection, conf):
    global log
    log.info('Initializing security groups')

    try:
        conf_groups = conf['security_groups']
    except KeyError:
        log.debug('No security groups to initialize')
        return

    current_groups = set(get_security_group_names(connection))
    target_groups = set(conf_groups.keys())

    groups_to_create = target_groups.difference(current_groups)

    result = []

    for name in groups_to_create:
        log.info('Creating security group \'%s\'', name)
        data = conf_groups[name]
        description = data.pop('description', None)

        group = create_security_group(connection, name, description)
        authorize_security_group(group, **data)
        result.append(group)

    return result
