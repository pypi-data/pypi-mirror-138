import json
from os.path import exists

from sonusai import logger


def load_mixdb(name: str) -> dict:
    if not exists(name):
        logger.error('{} does not exist'.format(name))
        exit()

    with open(name, encoding='utf-8') as f:
        mixdb = json.load(f)

    return mixdb
