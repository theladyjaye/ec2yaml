ec2yaml
========


Take a yaml file like this ::

    app:
      name: foo
      owner: adam venturella
      location: us-west-2
      key: <optional>
      secret: <optional>

    instances:
      app_server:
        key_name: aventurella
        image: ami-6ac2a85a
        size: m3.medium
        zone: us-west-2c
        tags:
          - key1: value1
          - key2: value2

        ip_address: foo

        security_groups:
          - ssh
          - http
          - https
          - foo-salt
          - foo-ssh

        volumes:
          - foo-volume: /dev/sdh

    elastic_ips:
      - foo

    volumes:
      foo-volume:
        size: 1
        zone: us-west-2c
        tags:
          - key1: value1
          - key2: value2


    security_groups:
      foo-ssh:
        ip_protocol: tcp
        from_port: 1022
        to_port: 1022
        cidr_ip: '0.0.0.0/0'

      foo-salt:
        ip_protocol: tcp
        from_port: 2000
        to_port: 65535
        cidr_ip: '0.0.0.0/0'


And materialize it into AWS EC2 accordingly.

Command line tool ::

    Usage:
    ec2yaml <conf> [(--key=<key> --secret=<secret>)\
    | --boto-profile=<boto-profile>]\
    [--loglevel=<level>]

    Options:
      -h --help                           Show this screen.
      -v --version                        Show version.
      -k --key=<key>                      AWS access key ID
      -s --secret=<secret>                AWS secret access key
      -bp --boto-profile=<boto-profile>   Boto Profile Name
      -l --loglevel=<level>               Log level to display [default: info]


