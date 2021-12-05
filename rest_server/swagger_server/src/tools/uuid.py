from uuid import UUID
from werkzeug.exceptions import NotAcceptable
import os


def is_valid_uuid(uuid_str):
    if isinstance(uuid_str, os.DirEntry):
        uuid_str = uuid_str.name
    try:
        UUID(uuid_str)
    except ValueError:
        return False
    return True


def check_uuid(uuid_str):
    if not is_valid_uuid(uuid_str):
        raise NotAcceptable(f"You provided an invalid UUID string: {uuid_str}")
