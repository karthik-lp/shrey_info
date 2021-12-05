import uuid
# from typing import List, Tuple, Optional, NewType, cast, Dict, Union, Callable
from pydantic import BaseModel
import datetime
# import yaml


class Family(BaseModel):
    id: uuid.UUID
    family_name: str
    total_members: int
    last_changed: datetime.datetime
