import unittest
from devbotaws.ec2 import utils
import devbotaws.ec2.security_groups as sg


class TestSecurityGroups(unittest.TestCase):

    def setUp(self):
        self.connection = utils.connection('us-west-2')

    def test_list_groups(self):
        out = sg.get_security_groups(self.connection)
        pass

