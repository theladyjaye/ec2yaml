import unittest
from devbotaws.ec2.elastic_ip import allocate_elastic_ip, release_elastic_ip
from boto.ec2.connection import EC2Connection


class TestElasticIp(unittest.TestCase):

    def test_create_elastic_ip(self):
        connection = EC2Connection()
        addy = allocate_elastic_ip(connection)
        self.assertIsNotNone(addy.public_ip)
        release_elastic_ip(connection, addy.public_ip)
