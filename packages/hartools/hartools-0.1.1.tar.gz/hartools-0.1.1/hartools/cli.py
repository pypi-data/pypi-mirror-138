"""Console script for hartools."""
import argparse
import sys

from datetime import date
from typing import Dict

from driconfig import DriConfig
from pydantic import BaseModel



def main():
    """Console script for hartools."""
    parser = argparse.ArgumentParser()
    #parser.add_argument('_', nargs='*')

    parser.add_argument('-yaml',metavar='config file in yaml format',
                        type=str,
                        default=None,
                        required=True)

    args = parser.parse_args()
    conf_file = args.yaml

    print("Arguments: " + str(args.yaml))
    #print("Arguments: " + str(args._))
    #print("Replace this message by putting your code into "
    #      "hartools.cli.main")
    #return 0
    #class DateInterval(BaseModel):
    #  """Model for the `date_interval` configuration."""
    #  start: date
    #  end: date
    #
    #
    #class AppConfig(DriConfig):
    #   """Interface for the config/config.yaml file."""
    #
    #   class Config:
    #       """Configure the YAML file location."""
    #       config_folder = "../examples"
    #       config_file_name = args.yaml
    #       model_parameters: Dict[str, float]
    #       #date_interval: DateInterval
    #   #print(Config.config_file_name)
    #config = AppConfig()
    #print(config.json(indent=4))
    #class Model(BaseModel):
    #  model: str

    #class AppConfig(DriConfig):
    #   """Interface for the config/config.yaml file."""
    #   class Config:
    #       """Configure the YAML file location."""
    #       config_folder = "."
    #       config_file_name = args.yaml
    #
    #   #model_parameters: Dict[str, float]
    #   #hartools_parameters: Dict[str,str,str]
    #   #hartools_parameters: Dict[str, float]
    #   model: Model
    #
    #config = AppConfig()
    #config = AppConfig(config_folder=".",config_file_name="config.yaml")
    #print(config.json(indent=4))
    #class Config:
    #    config_file_name = args.yaml
 
    #HarConfig = Config()

    class DateInterval(BaseModel):
      """Model for the `date_interval` configuration."""
      start: str
      end: str
    
    #ifile = "config_hartools.yaml"
    class HarConfig(DriConfig):
       """Interface for the config/config.yaml file."""
       class Config:
           """Configure the YAML file location."""
           config_folder = "."
           config_file_name = args.yaml
    
       model_data: Dict[str, str]
       date_interval: DateInterval
    
    HarToolsConf = HarConfig()
    print(HarToolsConf.json(indent=4))




if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
    #main()  # pragma: no cover
