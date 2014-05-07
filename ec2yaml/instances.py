import logging
import time
from . import utils

log = logging.getLogger(__name__)


def create_instance(
        connection,
        image_id,
        key_name=None,
        security_groups=None,
        instance_type='m1.small',
        **kwargs):
    return connection.run_instances(
        image_id,
        key_name=key_name,
        security_groups=security_groups,
        instance_type=instance_type,
        **kwargs)


def terminate_instance(connection, image_id):
    return connection.terminate_instances(image_id)


def instances_with_conf(connection, conf):
    global log
    log.info('Initializing instances, this can take a while')

    for key, value in conf['instances'].iteritems():
        reservation = create_instance(
            connection,
            value['image'],
            key_name=value['key_name'],
            security_groups=value.get('security_groups', None),
            instance_type=value['size'],
            placement=value.get('zone', None),
        )

        instance = reservation.instances[0]

        _wait_for_instance(instance)

        conf['instances'][key]['instance'] = instance

        log.info('Instance \'%s: %s\' has become available', instance.id, key)
        log.info('Instance available at \'%s\'', instance.public_dns_name)

        additional_tags = utils.process_group(value.get('tags', []))

        tag_instance_with_conf(
            connection, conf, instance, **additional_tags)


def tag_instance_with_conf(connection, conf, instance, **kwargs):
    global log

    tags = {
        'Name': conf['app']['name'],
        'Owner': conf['app']['owner']
    }

    tags.update(kwargs)

    log.info('Tagging instance \'%s\'', instance.id)
    log.debug('%s', tags)
    connection.create_tags([instance.id], tags)


def _wait_for_instance(instance):

    while True:
        if instance.public_dns_name:
            break

        try:
            instance.update()
        except:
            pass

        time.sleep(3)
