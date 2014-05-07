'''ec2yaml.

Usage:
  ec2yaml <conf> [(--key=<key> --secret=<secret>)] [--loglevel=<level>]

Options:
  -h --help              Show this screen.
  -v --version           Show version.
  -k --key=<key>         AWS access key ID
  -s --secret=<secret>   AWS secret access key
  -l --loglevel=<level>  Log level to display [default: info]
'''
import logging
from docopt import docopt
from . import __version__
from . import actions
from . import config


def _init_logging(level):

    logger = logging.getLogger('ec2yaml')
    logger.setLevel(getattr(logging, level, logging.INFO))
    logger.addHandler(logging.StreamHandler())


def _init_conf(args):
    conf = config.config_with_path(args['<conf>'])

    key = args.get('--key', None)
    secret = args.get('--secret', None)

    if key and secret in args:
        conf['app']['key'] = key
        conf['app']['secret'] = secret

    return conf


def main():

    version = 'ec2yaml {0}'.format(__version__)
    args = docopt(__doc__, version=version)

    _init_logging(args['--loglevel'].upper())

    conf = _init_conf(args)
    actions.initialize_with_conf(conf)


if __name__ == '__main__':
    main()
