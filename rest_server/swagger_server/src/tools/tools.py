import os
import yaml
from datetime import datetime
import numpy as np
from PIL import Image
from werkzeug.exceptions import (
    NotFound,
    Conflict,
    HTTPException,
    PreconditionFailed,
)
from swagger_server.src.tools.uuid import check_uuid
from swagger_server.src.config import BackendConfig
from distutils import dir_util
import time
import logging
import ruamel.yaml

log = logging.getLogger("swagger_server.__init__")


def get_base_data_base_path():
    p = BackendConfig.base_data_base_path
    if not os.path.exists(p):
        os.mkdir(p)
    return p


def get_families_base_path():
    return os.path.join(get_base_data_base_path(), "families")


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


# def update_zone_type(zone):
#     type_lookup = {
#         "RESTRICTED": NavigationZone.TYPE_RESTRICTED,
#         "AVOIDANCE": NavigationZone.TYPE_WEIGHTED,
#         "ONE_WAY": NavigationZone.TYPE_WEIGHTED,
#         "PREFERED_DIRECTION": NavigationZone.TYPE_WEIGHTED,
#         "ROBOT": NavigationZone.TYPE_WEIGHTED,
#         "MAX_VELOCITY": NavigationZone.TYPE_MAX_VELOCITY,
#         "NO_PASSING": NavigationZone.TYPE_TRIGGER,
#         "MAX_CAPACITY": NavigationZone.TYPE_INTERACTION,
#         "ERASER": NavigationZone.TYPE_FREE,
#     }
#     if isinstance(zone, Zone):
#         try:
#             zone.type = type_lookup[zone.ui_properties.visualization_type]
#         except Exception:
#             pass
#     elif (
#         isinstance(zone, dict)
#         and "ui_properties" in zone
#         and "visualization_type" in zone["ui_properties"]
#     ):
#         zone["type"] = type_lookup[zone["ui_properties"]["visualization_type"]]

#     return zone


def merge_dict(a, b, path=None, overwrite=True):
    "merges b into a"
    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_dict(a[key], b[key], path + [str(key)], overwrite)
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                if overwrite:
                    a[key] = b[key]
                else:
                    err_msg = "Overwrite flag is not set. Can not overwrite/modify the changes"
                    log.error(err_msg)
                    raise Conflict(err_msg)
        else:
            a[key] = b[key]
    return a


# def get_zones_list(environment_id):
#     env_path = get_env_path(environment_id)
#     poly_map_path = os.path.join(env_path, "polygon_maps")

#     zone_path = os.path.join(poly_map_path, "navigation_zones.yaml")
#     if not os.path.exists(zone_path):
#         return []
#     with open(zone_path) as f:
#         return yaml.load(f, Loader=yaml.SafeLoader)


def is_valid_env(environment_id):
    check_uuid(environment_id)
    return os.path.exists(os.path.join(get_env_base_path(), environment_id))
