from datetime import date
from typing import Dict

from driconfig import DriConfig
from pydantic import BaseModel


class DateInterval(BaseModel):
  """Model for the `date_interval` configuration."""
  start: str
  end: str

ifile = "config_hartools.yaml"  
class AppConfig(DriConfig):
   """Interface for the config/config.yaml file."""
   class Config:
       """Configure the YAML file location."""
       config_folder = "."
       config_file_name = ifile

   model_data: Dict[str, str]
   date_interval: DateInterval

config = AppConfig()
#config = AppConfig(config_folder=".",config_file_name="config.yaml")
print(config.json(indent=4))
