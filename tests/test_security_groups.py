import unittest
from devbotaws.ec2 import utils


class TestSecurityGroups(unittest.TestCase):


    def test_list_groups(self):
        connection = utils.connection()

