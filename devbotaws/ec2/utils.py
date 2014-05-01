from boto.ec2.connection import EC2Connection


__CONNECTION__ = None


def connection(location='us-east-1'):
    global __CONNECTION__

    if __CONNECTION__ is None:
        __CONNECTION__ = EC2Connection(location)

    return __CONNECTION__


def connection_from_config(conf):
    location = conf['app'].get('location', 'us-east-1')
    return connection(location=location)
