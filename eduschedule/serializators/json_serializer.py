import json

def serialize(dict_):
    return json.dumps(dict_, indent=4, sort_keys=True, default=str)