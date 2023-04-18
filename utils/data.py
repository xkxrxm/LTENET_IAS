from itertools import islice
from typing import Iterator

import models

upload_dict = dict()


def batch(it: Iterator, size):
    return iter(lambda: tuple(islice(it, size)), ())


def str2schemas(table_name: str, **kwargs):
    try:
        return schemas.tb.__dict__[table_name](**kwargs)
    except Exception:
        raise


def str2models(table_name: str, **kwargs):
    try:
        return models.tb.__dict__[table_name](**kwargs)
    except Exception:
        raise
