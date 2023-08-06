from copy import deepcopy
from typing import List
from typing import Union

from sonusai import logger
from sonusai.mixture import get_mixtures_from_mixid


def new_mixdb_from_mixid(mixdb: dict,
                         mixid: Union[str, List[int]]) -> dict:
    mixdb_out = deepcopy(mixdb)
    mixdb_out['mixtures'] = get_mixtures_from_mixid(mixdb_out['mixtures'], mixid)

    if not mixdb_out['mixtures']:
        logger.error('Error processing mixid: {}; resulted in empty list of mixtures'.format(mixid))
        exit()

    return mixdb_out
