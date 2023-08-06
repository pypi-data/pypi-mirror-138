import logging
from os import getcwd
from os.path import dirname

__version__ = '0.3.16'
basedir = dirname(__file__)

# create logger
logger = logging.getLogger('sonusai')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


# create file handler
def create_file_handler(filename: str):
    fh = logging.FileHandler(filename=filename, mode='w')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)


# update console handler
def update_console_handler(verbose: bool):
    if not verbose:
        logger.removeHandler(console_handler)
        console_handler.setLevel(logging.INFO)
        logger.addHandler(console_handler)


# write initial log message
def initial_log_messages(name: str):
    from datetime import datetime
    from getpass import getuser
    from socket import gethostname

    logger.info('SonusAI {} {}'.format(name, __version__))
    logger.debug('Host:      {}'.format(gethostname()))
    logger.debug('User:      {}'.format(getuser()))
    logger.debug('Directory: {}'.format(getcwd()))
    logger.debug('Date:      {}'.format(datetime.now()))
    logger.debug('')
