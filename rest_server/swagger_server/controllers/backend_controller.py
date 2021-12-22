from swagger_server.src.config import BackendConfig
from swagger_server.controllers.family_controller import FamilyController
from swagger_server.src.tools.tools import (
    get_families_base_path,
    # get_my_family_id,
    get_fam,
    get_fam_path,
    serialize_metadata,
)
from swagger_server.src.tools.uuid import check_uuid, is_valid_uuid
from werkzeug.exceptions import (
    InternalServerError,
    NotFound,
)

import os
import logging

log = logging.getLogger("swagger_server.backend_controller")


class BackEndController:

    __instance = None  # needed for singleton class
    __my_family_id = None
    __family_controller_list = None
    __max_length = None

    @staticmethod
    def get_instance():
        """get_instance

        Returns the singleton class instance if it is instantiated.


        :rtype: BackEndController
        """
        if BackEndController.__instance is None:
            BackEndController()
        return BackEndController.__instance

    def __init__(self):
        if BackEndController.__instance is not None:
            raise Exception("This is a singleton class")
        else:

            self.__family_controller_list = []
            self.__max_length = 3
            self.__my_family_id = self.get_my_family_id()
            BackEndController.__instance = self
            if self.__my_family_id is not None:
                self.__family_controller_list.append(
                    FamilyController(id=self.__my_family_id)
                )

    def add_family(self, friendly_name=""):
        """add_family

        Adds a new family

        :param friendly_name:
        :type friendly_name: str

        :rtype: Family
        """
        # fam = self.__family_controller_list[0].create_family(
        #     friendly_name)
        # self.__family_controller_list.append(
        #     FamilyController(id=self.__my_family_id)
        # )
        fam = FamilyController(name=friendly_name).get_self_family()
        serialize_metadata(fam, get_families_base_path())
        try:
            self.update_my_family_marker(fam.id)
            self.update_list(fam.id, 0)
            self.__my_family_id = fam.id
            print(self.__my_family_id)
        except Exception as e:
            self.__my_family_id = None
            FamilyController.delete_family_for_family_id(fam.id)
            log.error(str(e))
            raise e
        return f"This is the new added family {fam.friendly_name}: {fam.id}"

    def get_families_lists(self):
        """get_families_lists

        Returns the family ID of the family from the family_controller.


        :rtype: Str
        """
        fam_list_string = "List: "
        if not self.__family_controller_list:
            return "Families list is empty"
        for fam in self.__family_controller_list:
            fam_list_string += f"{fam.getID()}, "
        return fam_list_string

    def get_family_index_from_list(self, family_id):
        """get_family_index_from_list

        Search for a controller in the family_controller list for a specific ID.
        If nothings match, it returns None


        :rtype: int
        """
        for index, controller in enumerate(self.__family_controller_list):
            if controller.getID() == family_id:
                return index
        return None

    def update_list(self, family_id, update_index=1):
        """update_list

        Update the position in the list of an FamilyController for the given family_id.
        If the current position is lower equal the update_index, it will not change the position and returns the controller back.
        If there is no controller for the given family_id, then it instantiates a FamilyController.


        :rtype: FamilyController
        """
        check_uuid(family_id)
        index = self.get_family_index_from_list(family_id)
        if index is not None:
            if index > update_index:
                family_controller = self.__family_controller_list.pop(index)
            else:
                return self.__family_controller_list[index]
        else:
            if len(self.__family_controller_list) >= self.__max_length:
                self.__family_controller_list.pop()
            family_controller = FamilyController(id=family_id)
        self.__family_controller_list.insert(update_index, family_controller)
        return family_controller

    def get_families(self):
        """get_familys

        List all available family ids


        :rtype: List[UUID]
        """
        with os.scandir(get_families_base_path()) as it:
            families = [
                self.get_families_family_id(entry.name)
                for entry in it
                if (
                    entry.is_dir()
                    and is_valid_uuid(entry)
                    and os.path.exists(
                        os.path.join(get_fam_path(entry), "metadata.yaml")
                    )
                )
            ]
        return families

    def get_families_family_id(self, family_id):
        """get_families_family_id

        Get the information for one family

        :param family_id:
        :type family_id: str

        :rtype: Family
        """
        check_uuid(family_id)

        return get_fam(family_id)

    def get_family_controller(self, family_id):
        """get_family_controller

        Method for testing: Returns the family_controller for a given ID


        :rtype: FamilyController
        """
        for fam in self.__family_controller_list:
            if str(fam.getID()) == family_id:
                print(f"Family id: {fam.getID()}")
                return fam
        return None

    def get_family(self, family_id):
        """get_family

        Get the information for one family

        :param family_id:
        :type family_id: str

        :rtype: Family
        """
        check_uuid(family_id)
        return self.update_list(family_id).get_self_family()

    def get_my_family_id(self):
        my_family_marker = os.path.join(get_families_base_path(), "my_family")
        try:
            with open(my_family_marker) as f:
                lines = f.readlines()
            my_family_id = lines[0].split()[0]
            return my_family_id if is_valid_uuid(my_family_id) else None
        except IOError:
            return

    def set_my_family(self, family_id):
        """set_my_family

        Set as my family.


        :rtype: Family
        """
        self.update_my_family_marker(family_id)
        index = self.get_family_index_from_list(family_id)
        if index is not None:  # Controller already axists for this Family
            if index > 0:
                family_controller = self.__family_controller_list.pop(index)
                self.__family_controller_list.insert(0, family_controller)
        else:
            if len(self.__family_controller_list) >= self.__max_length:
                self.__family_controller_list.pop()
            family_controller = FamilyController(id=family_id)
            self.__family_controller_list.insert(0, family_controller)
        self.__my_family_id = family_id
        return self.my_family_get()

    def update_my_family_marker(self, family_id):
        """update_my_family_marker

        Update the my_family file with the new ID.


        :rtype: None
        """
        self.my_family_delete()
        fam_path = get_fam_path(family_id)
        if not (os.path.exists(fam_path)):
            err_msg = f"Family not found. {fam_path} folder does not exist"
            log.error(err_msg)
            raise NotFound(err_msg)
        my_family_marker = os.path.join(get_families_base_path(), "my_family")
        with open(my_family_marker, "w") as f:
            f.writelines(family_id)

    def my_family_get(self):
        """my_family_get

        Returns my Family.


        :rtype: Family
        """
        if self.__my_family_id is None:
            err_msg = "No family is added to as your family"
            log.error(err_msg)
            raise NotFound(err_msg)
        return get_fam(self.__my_family_id)        

    def my_family_delete(self):
        """my_family_delete

        Removes my_family marker/file.


        :rtype: Str, HTML_code
        """
        my_family_marker = os.path.join(get_families_base_path(), "my_family")
        if not os.path.exists(my_family_marker):
            return "OK", 200

        os.remove(my_family_marker)
        return "OK", 200
