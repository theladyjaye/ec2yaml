import unittest
from devbotaws.ec2 import utils
import devbotaws.ec2.security_groups as sg


class TestSecurityGroups(unittest.TestCase):

    def setUp(self):
        self.connection = utils.connection('us-west-2')

    def test_get_security_groups(self):
        out = sg.get_security_groups(self.connection)

        for g in out:
            # will fail in python 3
            self.assertTrue(hasattr(g, 'name'))

    def test_get_security_group_names(self):
        out = sg.get_security_group_names(self.connection)

        for name in out:
            # will fail in python 3
            self.assertTrue(isinstance(name, basestring))
