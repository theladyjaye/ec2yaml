import unittest
from devbotaws.ec2 import config
from devbotaws.ec2.utils import connection
from devbotaws.ec2.instances import create_instance, terminate_instance


class TestCreateInstance(unittest.TestCase):

    def test_create_instance(self):
        conf = config.load_config('resources/sample.conf')

        conn = connection()
        example_instance = conf['instances']['app_server']

        reservation = create_instance(
            conn,
            'ami-36d6b006',
            key_name='dpec2',
            # security_groups=example_instance['security_groups'],
            instance_type=example_instance['size']
        )

        terminate_instance(conn, reservation.instances[0].id)
