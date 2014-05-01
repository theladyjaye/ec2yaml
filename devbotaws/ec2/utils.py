import boto.ec2


__CONNECTION__ = None


def connection(location='us-east-1'):
    global __CONNECTION__

    if __CONNECTION__ is None:
        __CONNECTION__ = boto.ec2.connect_to_region(location)

    return __CONNECTION__


def connection_from_config(conf):
    location = conf['app'].get('location', 'us-east-1')
    return connection(location=location)
