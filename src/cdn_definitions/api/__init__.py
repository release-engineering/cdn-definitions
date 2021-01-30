import os
import json
from .. import load_data


def schema():
    with open(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "schema.json")
    ) as f:
        return json.load(f)


def data(source=None):
    return load_data(source)
