import uuid
from pydantic import BaseModel
import datetime


class Family(BaseModel):
    id: uuid.UUID
    family_name: str
    total_members: int
    last_changed: datetime.datetime
