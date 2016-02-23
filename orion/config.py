import json
import os

class Option():
    def __init__(self, d):
        self.__dict__ = d

config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)) + "/config.json"

options = Option(json.loads(open(config_path).read()))