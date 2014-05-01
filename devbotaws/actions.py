from devbotaws.ec2 import config
from devbotaws.ec2.instances import instances_from_config
from devbotaws.ec2.utils import connection_from_config
from devbotaws.ec2.elastic_ip import allocate_elastic_ip_with_conf


def initialize_with_conf(path):
    conf = config.load_config(path)
    conn = connection_from_config(conf)
    allocate_elastic_ip_with_conf(conn, conf)
    # create security groups
    # @adam NEED TO ADD THIS

    ##  create instance and apply security groups
    # this will set the conf['instances']['foo']['instance'] to the instance
    instances_from_config(connection, conf)



# - create/apply tags for instance
# - apply elastic ip to instance
# - return the addition to a users ~/.ssh/config file:
#     - ex:
#         Host cableknit
#            HostName 54.203.255.168
#            User ubuntu
#            IdentityFile ~/.ssh/dpec2.pem
