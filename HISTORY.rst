.. :changelog:

Release History
---------------

0.0.1 (2014-05-07)
++++++++++++++++++

**API Changes**
**Bugfixes**


0.0.6 (2014-05-07)
++++++++++++++++++

**API Changes**
- Instances can now be arbitrarily tagged ::

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

- Volumes can now be arbitrarily tagged ::

    volumes:
      foo-volume:
        size: 1
        zone: us-west-2c
        tags:
          - key1: value1
          - key2: value2


0.0.8 (2014-05-08)
++++++++++++++++++

**API Changes**
- A boto profile can now be specified in the command line arguments

**Bugfixes**
- Fixes an issue with a key and secret from the command line not
  being properly assigned.
