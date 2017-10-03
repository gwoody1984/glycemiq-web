import configparser
import json
import os

config = configparser.ConfigParser()
basedir = os.path.abspath(os.path.dirname(__file__))
jsonConfig = os.path.join(basedir, 'config.json')

if os.path.exists(jsonConfig):
    with open(jsonConfig, 'r') as file:
        config = json.load(file)
else:
    raise IOError('config.json not present in ' + basedir)


def config_as_dict(section):
    return dict(config.get(section))


def config_as_obj(section):
    return _Config(config_as_dict(section))


class _Config:
    def __init__(self, kvp):
        for item in kvp.keys():
            setattr(self, item, kvp[item])
