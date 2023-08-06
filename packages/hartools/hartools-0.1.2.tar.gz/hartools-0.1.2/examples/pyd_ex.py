from pydantic import BaseModel
from typing import Optional, List
from pydantic import BaseSettings, DirectoryPath


class Person(BaseModel):
    first_name: str
    last_name: str
    interest: Optional[List[str]]
data = {"first_name": "Ahmed", "last_name": "Besbes"}
person = Person(**data)
print(person)

class Model(BaseModel):
    user: str
    ecfspath: str
    localpath: DirectoryPath

data = {"user": "nhd", "ecfspath": "ec:/nhd/", "localpath" : "/home/cap"}
model = Model(**data)
print(model)

