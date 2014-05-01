

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
