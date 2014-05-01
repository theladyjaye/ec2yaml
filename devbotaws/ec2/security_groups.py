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

    kwargs = {
        'ip_protocol': ip_protocol,
        'from_port': from_port,
        'to_port': to_port,
    }

    if cidr_ip:
        kwargs['cidr_ip'] = cidr_ip

    if src_group:
        kwargs['src_group'] = src_group

    group.authorize(**kwargs)


def _add_to_cached_groups(group):
    global GROUPS

    if GROUPS is None:
        GROUPS = [group]
    else:
        GROUPS.append(group)


def create_application_security_group(connection, name, description=None):
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

