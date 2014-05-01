

def allocate_elastic_ip(connection):
    return connection.allocate_address()


def release_elastic_ip(connection, ip_address):
    return connection.release_address(ip_address)
