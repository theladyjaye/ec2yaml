import unittest
from devbotaws.ec2 import utils


class TestUtils(unittest.TestCase):

    def test_key_for_group_with_string(self):
        key = utils.key_for_group('foo')
        self.assertTrue(key == 'foo')

    def test_key_for_group_with_dict(self):
        key = utils.key_for_group({'foo': 'bar'})
        self.assertTrue(key == 'foo')

    def test_value_for_group_with_string(self):
        value = utils.value_for_group('foo')
        self.assertTrue(value is None)

    def test_value_for_group_with_dict(self):
        value = utils.value_for_group({'foo': 'bar'})
        self.assertTrue(value == 'bar')

    def test_process_group(self):
        out = utils.process_group([
            {'foo': 1},
            'bar',
            {'baz': 2}
        ])

        self.assertTrue('foo' in out)
        self.assertTrue('bar' in out)
        self.assertTrue('baz' in out)

        self.assertTrue(out['foo'] == 1)
        self.assertTrue(out['bar'] is None)
        self.assertTrue(out['baz'] == 2)

