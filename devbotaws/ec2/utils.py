from boto.ec2.connection import EC2Connection


__CONNECTION__ = None


def connection():
    global __CONNECTION__

    if __CONNECTION__ is None:
        __CONNECTION__ = EC2Connection()

    return __CONNECTION__
