import os
import yaml
from datetime import datetime
from werkzeug.exceptions import (
    NotFound,
    Conflict)
from swagger_server.src.tools.uuid import check_uuid
from swagger_server.src.config import BackendConfig
from swagger_server.models.family import Family
# from swagger_server.schema_generator import Family
import logging

log = logging.getLogger("swagger_server.__init__")


def get_base_data_base_path():
    p = BackendConfig.base_data_base_path
    if not os.path.exists(p):
        os.mkdir(p)
    return p


def get_families_base_path():
    families_folder_path = os.path.join(get_base_data_base_path(), "families")
    if not os.path.exists(families_folder_path):
        os.mkdir(families_folder_path)
    return families_folder_path


def werkzeug_to_pair(we):
    return (f"{we.name}: {we.description}", we.code)


def create_fam_folder(family, base_directory):
    os.mkdir(os.path.join(base_directory, family.id))


def serialize_metadata(family, base_directory):
    family.last_changed = datetime.now().isoformat()
    with open(os.path.join(base_directory, family.id, "metadata.yaml"), "w+") as f:
        yaml.dump(family.to_dict(), f)


def get_my_family_id():
    my_family_marker = os.path.join(get_families_base_path(), "my_family")
    with open(my_family_marker) as f:
        lines = f.readlines()
    return lines[0].split()[0]


def check_my_family(target_fam):
    try:
        ae = get_my_family_id()
    except FileNotFoundError:
        err_msg = "No faimly is added as your family."
        log.error(err_msg)
        raise NotFound(err_msg)
    if ae != target_fam:
        raise Conflict(
            f'The requested family ID ("{target_fam}") '
            + f'is not listed as YOUR family ("{ae}")'
        )


def is_my_family(family_id):
    try:
        current_my_family = get_my_family_id()
        if family_id == current_my_family:
            return True
        else:
            return False
    except FileNotFoundError:
        return False


def dir_to_fam(directory):
    with open(os.path.join(directory, "metadata.yaml")) as f:
        d = yaml.safe_load(f)
        fam = Family.from_dict(d)
    return fam


def get_fam_path(family_id, ignore_not_found=False):
    check_uuid(family_id)
    fam_path = os.path.join(get_families_base_path(), family_id)
    if not ignore_not_found and not os.path.exists(fam_path):
        err_msg = f"Family {family_id} does not exist"
        log.error(err_msg)
        raise NotFound(err_msg)
    return fam_path


def get_fam(family_id):
    return dir_to_fam(get_fam_path(family_id))


def is_valid_fam(family_id):
    check_uuid(family_id)
    return os.path.exists(os.path.join(get_families_base_path(), family_id))
