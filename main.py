import sys
import logging
from devbotaws import actions


def main(path):
    logger = logging.getLogger('devbotaws')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    actions.initialize_with_path(path)

if __name__ == '__main__':
    main(sys.argv[1])
