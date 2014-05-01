import unittest
from devbotaws.ec2.utils import connection
from devbotaws.ec2.elastic_ip import allocate_elastic_ip, release_elastic_ip


class TestElasticIp(unittest.TestCase):

    def test_create_elastic_ip(self):
        conn = connection()
        addy = allocate_elastic_ip(conn)
        self.assertIsNotNone(addy.public_ip)
        release_elastic_ip(conn, addy.public_ip)
