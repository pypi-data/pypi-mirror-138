from datetime import date
from typing import Dict

from driconfig import DriConfig
from pydantic import BaseModel


class DateInterval(BaseModel):
  """Model for the `date_interval` configuration."""
  start: date
  end: date

  
class AppConfig(DriConfig):
   """Interface for the config/config.yaml file."""
   class Config:
       """Configure the YAML file location."""
       config_folder = "."
       config_file_name = "config.yaml"

   model_parameters: Dict[str, float]
   date_interval: DateInterval

config = AppConfig()
#config = AppConfig(config_folder=".",config_file_name="config.yaml")
print(config.json(indent=4))
