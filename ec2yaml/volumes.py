import logging
from . import utils

log = logging.getLogger(__name__)


def volumes_with_conf(connection, conf):
    global log

    log.info('Initializing EBS volumes')
    try:
        volumes = conf['volumes']
    except KeyError:
        log.debug('No EBS volumes to initialize')
        return

    for key, value in volumes.iteritems():
        log.info('Creating EBS Volume \'%s\'', key)

        kwargs = {
            'size': int(value.get('size')),
            'zone': value['zone']  # required
        }

        result = create_volume(connection, **kwargs)
        value['volume'] = result
        tag_volume_with_conf(connection, conf, result)


def assign_volumes_with_conf(conf):
    global log

    volumes = conf['volumes']
    instances = conf['instances']

    log.info('Assigning volumes to instances')

    for i_name, i_values in instances.iteritems():
        i_volumes = utils.process_group(i_values.get('volumes', []))

        for name, device in i_volumes.iteritems():
            target = volumes.get(name, None)

            if not target:
                log.debug('Unable to assign volume \'{0}\' '
                          'to instance \'{1}\''.format(name, i_name))
                continue

            target['volume'].attach(i_values['instance'].id, device)

            log.info('Assigned volume \'{0}\' '
                     'to instance \'{1}\' @ \'{2}\''
                     .format(name, i_name, device))


def create_volume(
        connection,
        size,
        zone,
        snapshot=None,
        volume_type=None,
        iops=None):
    '''
    :param connection: the ec2 creation to use
    :type connection: boto.ec2.connection.EC2Connection

    :param size: The size of the new volume, in GiB
                 1GiB ~ 1.074GB ~ 1,073,741,824 Bytes
    :type size: int

    :param zone: The availability zone in which the Volume will be created.
    :type zone: string or boto.ec2.zone.Zone

    :param snapshot: The snapshot from which the new Volume will be created.
    :type snapshot: string or boto.ec2.snapshot.Snapshot

    :param volume_type: The type of the volume. (optional). Valid values are: standard | io1.
    :type volume_type: string

    :param iops: The provisioned IOPs you want to associate with this volume. (optional)
    :type iops: int
    '''
    return connection.create_volume(
        size,
        zone,
        snapshot=snapshot,
        volume_type=volume_type,
        iops=iops)


def tag_volume_with_conf(connection, conf, volume):
    global log

    tags = {
        'Name': conf['app']['name'],
        'Owner': conf['app']['owner']
    }

    log.info('Tagging volume \'%s\'', volume.id)
    log.debug('%s', tags)
    connection.create_tags([volume.id], tags)
