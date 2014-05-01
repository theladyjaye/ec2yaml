import unittest
from nose.tools import nottest
from nose.tools import raises
from devbotaws.ec2 import utils


class TestEC2(unittest.TestCase):

    def test_config_succeeds(self):
        conf = utils.load_config('resources/sample.conf')

        self.assertTrue(conf['app'] == 'foo')
        self.assertTrue(conf['instances']['app_server'] is not None)

    @raises(IOError)
    def test_config_fails_not_found(self):
        utils.load_config('resources/missing')
