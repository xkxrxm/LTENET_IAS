from itertools import islice
from typing import Iterator

import app.models.tb
import app.schemas.tb

upload_dict = dict()


def batch(it: Iterator, size):
    return iter(lambda: tuple(islice(it, size)), ())


def str2schemas(table_name: str, **kwargs):
    try:
        return app.schemas.tb.__dict__[table_name](**kwargs)
    except Exception:
        raise


def str2models(table_name: str, **kwargs):
    try:
        return app.models.tb.__dict__[table_name](**kwargs)
    except Exception:
        raise
