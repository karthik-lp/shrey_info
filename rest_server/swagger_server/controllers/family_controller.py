from uuid import uuid4
from swagger_server.controllers.members_controller import MembersController
from swagger_server.models.family import Family
# from swagger_server.schema_generator import Family

from swagger_server.src.tools.tools import (
    get_families_base_path,
    get_my_family_id,
    get_fam,
    get_fam_path,
    is_my_family,
    werkzeug_to_pair,
    create_fam_folder,
    serialize_metadata,
    )

from swagger_server.src.tools.uuid import (
    is_valid_uuid,
    check_uuid,
)

from werkzeug.exceptions import (
    HTTPException,
    NotFound,
    Forbidden,
)
from shutil import rmtree
import logging
import os
from datetime import datetime
log = logging.getLogger("swagger_server.family_controller")


class FamilyController:
    __name = None
    __id = None
    __family = None
    __members_controller = None


    @staticmethod
    def delete_family_for_family_id(family_id):
        """delete_family

        Delete one family

        :param family_id: In UUID format.
        :type family_id: str

        :rtype: Family
        """
        if is_my_family(family_id):
            err_msg = f"Cannot delete my family: {family_id}."
            log.error(err_msg)
            raise Forbidden(err_msg)
        try:
            fam_path = get_fam_path(family_id)
        except HTTPException as e:
            return werkzeug_to_pair(e)
        rmtree(fam_path)
        return f"Removed family {family_id}", 200

    @staticmethod
    def get_families():
        """get_families

        List all available family ids


        :rtype: List[UUID]
        """
        with os.scandir(get_families_base_path()) as it:
            fams = [
                FamilyController.get_family(entry.name)
                for entry in it
                if (
                    entry.is_dir()
                    and is_valid_uuid(entry)
                    and os.path.exists(
                        os.path.join(get_fam_path(entry), "metadata.yaml")
                    )
                )
            ]
        return fams

    @staticmethod
    def get_family(family_id):
        """get_family

        Get the information for one family

        :param family_id:
        :type family_id: str

        :rtype: Family
        """
        check_uuid(family_id)

        return get_fam(family_id)

    @staticmethod
    def delete_families(my_family_id=None):
        """delete_families

        Delete all families

        :rtype: divt[str]
        """

        fams = FamilyController.get_families()
        try:
            if my_family_id is None:
                my_family_id = get_my_family_id()
            msg = (
                "Deleting all families except "
                + f"my_family: {my_family_id}"
            )
            log.warning(msg)
            for fam in fams:
                if not fam.id == my_family_id:
                    try:
                        fam_path = get_fam_path(fam.id)
                    except NotFound:
                        err_msg = (
                            f"Path to Family {fam.id}"
                            + "was not found. Cannot delete it."
                        )
                        log.warning(err_msg)
                        continue
                    rmtree(fam_path)
            response = {"response_msg": msg}
        except FileNotFoundError:
            msg = "Deleting all existing families"
            log.warning(msg)
            for fam in fams:
                try:
                    fam_path = get_fam_path(fam.id)
                except NotFound:
                    err_msg = (
                        f"Path to Family {fam.id}"
                        + "was not found. Can not delete it."
                    )
                    log.warning(err_msg)
                    continue
                rmtree(fam_path)
            response = {"response_msg": msg}

        return response, 200

    def __init__(self, name=None, id=None):
        self.__name = name
        if id is None:
            # Create new Family
            self.__family = self.create_family(name)
            serialize_metadata(self.__family, get_families_base_path())
            self.__id = self.__family.id
        else:
            # Load the Family
            check_uuid(id)
            self.__id = id
            self.__family = FamilyController.get_family(self.__id)
        # Load the member controller
        self.__members_controller = MembersController()

    def create_family(self, friendly_name=""):
        """create_family

        Create a new Family with a random UUID4

        :rtype: Family
        """
        print(friendly_name)
        fam = Family(
            id=str(uuid4()),
            friendly_name=friendly_name if friendly_name is not None else "",
            total_members=0,
            last_changed=datetime.now().isoformat(),
        )
        create_fam_folder(fam, get_families_base_path())
        return fam

    def getName(self):
        return self.__name

    def getID(self):
        return self.__id

    def getMembersController(self):
        return self.__members_controller

    def delete_family(self):
        """delete_family

        Delete the family from this controller

        :rtype: Family
        """
        return FamilyController.delete_family_for_family_id(self.__id)

    def get_self_family(self):
        return self.__family
