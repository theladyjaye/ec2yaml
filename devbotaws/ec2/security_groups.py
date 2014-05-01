

def get_security_groups(connection):
    rs = connection.get_all_security_groups()


def authorize_securitygroup(group_id, ip_protocol, from_port, to_port,
                            src_group=None, cidr_ip=None):

    params = {'Action': 'AuthorizeSecurityGroupIngress'}
    params['GroupId'] = group_id
    params['IpPermissions.1.IpProtocol'] = ip_protocol
    params['IpPermissions.1.FromPort'] = from_port
    params['IpPermissions.1.ToPort'] = to_port

    if src_group:
        params['IpPermissions.1.Groups.1.GroupId'] = src_group
    elif cidr_ip:
        params['IpPermissions.1.IpRanges.1.CidrIp'] = cidr_ip

    location = get_location()
    result = query(params, location=location, return_root=True)

    if 'error' in result:
        code = result['error']['Errors']['Error']['Code']
        if code != 'InvalidGroup.Duplicate':
            log.error(result)
            return None
