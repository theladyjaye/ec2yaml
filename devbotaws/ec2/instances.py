import logging


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
    log.info('Initializing instances')
    for key in conf['instances']:
        value = conf['instances'][key]
        reservation = create_instance(
            connection,
            value['image'],
            key_name=value['key_name'],
            security_groups=value.get('security_groups', None),
            instance_type=value['size']
        )

        conf['instances'][key]['instance'] = reservation.instances[0]
