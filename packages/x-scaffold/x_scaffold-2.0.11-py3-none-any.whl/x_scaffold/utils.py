import json
import os


def read_json(path, default_value):
    if path and os.path.exists(path) and os.path.isfile(path):
        with open(path, 'r') as fhd:
            return json.load(fhd)
    return default_value
