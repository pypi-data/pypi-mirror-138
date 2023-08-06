# Class to store global configuration variables
from __future__ import absolute_import
from pathlib import Path,PurePath
import os
import sys
from os import path
#sys.path.append(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
#sys.path.insert(0, os.path.abspath('./harmon/'))

#CONFIG_FILE=os.path.join(sys.path[-1],"streams_cca.yaml")
env_conf = os.getenv("HARMONCONF_YML")
if env_conf is None:
    basedir = f'{os.path.abspath(__file__+"/..")}'
    CONFIG_FILE=f"{basedir}/streams.yaml"
else:
    CONFIG_FILE=env_conf

#print(f"CONFIG: using {CONFIG_FILE} for input")
class streams_info():      # for database globals
    def __init__(self, yaml_file = CONFIG_FILE):
        self.yaml_file = yaml_file
        self.yaml = self.read_yaml()

    def read_yaml(self):
        import yaml
        with open(self.yaml_file, "r") as f:
            return yaml.safe_load(f)

global harmonconf
harmonconf = streams_info()

def init_config():
    '''
    Initializes a ConfigParser instance
    @return No return value
    '''
    global cp
    cp=ConfigParser.RawConfigParser()

if __name__ == '__main__':
    init_config()
