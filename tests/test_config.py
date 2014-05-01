import unittest
from nose.tools import nottest
from nose.tools import raises
from devbotaws.ec2 import config
from devbotaws.ec2 import errors


class TestConfig(unittest.TestCase):

    def test_config_succeeds(self):
        conf = config.config_with_path('resources/sample.conf')

        self.assertTrue(conf['app']['name'] == 'foo')
        self.assertTrue(conf['instances']['app_server'] is not None)

    @raises(IOError)
    def test_config_fails_not_found(self):
        config.config_with_path('resources/missing')

    @raises(errors.InvalidConfig)
    def test_config_validation_invalid_app(self):
        conf = {}
        config.validate_config(conf)

    @raises(errors.InvalidConfig)
    def test_config_validation_invalid_name_or_owner_missing(self):
        conf = {'app': {}}
        config.validate_config(conf)

    @raises(errors.InvalidConfig)
    def test_config_validation_invalid_name_or_owner_none(self):
        conf = {'app': {'name': None, 'owner': None}}
        config.validate_config(conf)

    @raises(errors.InvalidConfig)
    def test_config_validation_invalid_missing_owner(self):
        conf = {'app': {'name': 'foo'}}
        config.validate_config(conf)

    @raises(errors.InvalidConfig)
    def test_config_validation_invalid_missing_name(self):
        conf = {'app': {'owner': 'foo'}}
        config.validate_config(conf)

    def test_config_validation_valid(self):
        conf = {'app': {'owner': 'foo', 'name': 'bar'}}

        try:
            config.validate_config(conf)
        except errors.InvalidConfig as e:
            self.fail('Invalid Config: {0}'.format(e.message))

