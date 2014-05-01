import unittest
from devbotaws.ec2 import utils
import devbotaws.ec2.security_groups as sg
from devbotaws.ec2 import config


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

    def test_create_security_group_with_cidr(self):
        sg.create_security_group(self.connection, 'foo')

        groups = sg.get_security_group_names(self.connection, refresh=True)
        self.assertTrue('foo' in groups)

        result = sg.delete_security_group(self.connection, 'foo')
        self.assertTrue(result)

    def test_authorize_security_group(self):
        conn = self.connection

        group = sg.create_security_group(conn, 'foo')

        sg.authorize_security_group(
            group,
            ip_protocol='tcp',
            from_port=2000,
            to_port=4000,
            cidr_ip='0.0.0.0/0')

        all_groups = sg.get_security_groups(conn, refresh=True)
        target = next(x for x in all_groups if x.name == 'foo')

        result = sg.delete_security_group(conn, 'foo')
        self.assertTrue(result)

        perm = target.rules[0]

        self.assertTrue(perm.ip_protocol == 'tcp')
        self.assertTrue(perm.from_port == '2000')
        self.assertTrue(perm.to_port == '4000')
        self.assertTrue(perm.grants[0].cidr_ip == '0.0.0.0/0')

    def test_authorize_security_group_with_group_grant(self):
        conn = self.connection

        group = sg.create_security_group(conn, 'foo')

        sg.authorize_security_group(
            group,
            ip_protocol='tcp',
            from_port=2000,
            to_port=4000,
            src_group=group)

        all_groups = sg.get_security_groups(conn, refresh=True)
        target = next(x for x in all_groups if x.name == 'foo')

        result = sg.delete_security_group(conn, 'foo')
        self.assertTrue(result)

        perm = target.rules[0]

        self.assertTrue(perm.ip_protocol == 'tcp')
        self.assertTrue(perm.from_port == '2000')
        self.assertTrue(perm.to_port == '4000')
        self.assertTrue(perm.grants[0].group_id == target.id)

    def test_create_application_security_group(self):
        conn = self.connection
        sg.create_application_security_group(conn, 'foo')

        all_groups = sg.get_security_groups(conn, refresh=True)
        target = next(x for x in all_groups if x.name == 'foo')

        result = sg.delete_security_group(conn, 'foo')
        self.assertTrue(result)

        self.assertTrue(len(target.rules) == 3)

        def assertTCP_or_UDP(perm):
            self.assertTrue(perm.ip_protocol == 'tcp' or perm.ip_protocol == 'udp')
            self.assertTrue(perm.from_port == '1')
            self.assertTrue(perm.to_port == '65535')
            self.assertTrue(perm.grants[0].group_id == target.id)

        def assertICMP(perm):
            self.assertTrue(perm.ip_protocol == 'icmp')
            self.assertTrue(perm.from_port == '-1')
            self.assertTrue(perm.to_port == '-1')
            self.assertTrue(perm.grants[0].group_id == target.id)

        for each in target.rules:
            if each.ip_protocol == 'tcp' or each.ip_protocol == 'udp':
                assertTCP_or_UDP(each)

            else:
                assertICMP(each)

    def test_security_groups_with_conf(self):
        conn = self.connection
        conf = config.load_config('resources/sample.conf')
        sg.security_groups_with_conf(conn, conf)

        all_groups = sg.get_security_group_names(conn, refresh=True)

        self.assertTrue('foo-ssh' in all_groups)
        self.assertTrue('foo-salt' in all_groups)

        sg.delete_security_group(conn, 'foo-ssh')
        sg.delete_security_group(conn, 'foo-salt')




