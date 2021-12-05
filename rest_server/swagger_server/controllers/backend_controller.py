from swagger_server.src.config import BackendConfig
from swagger_server.controllers.family_controller import FamilyController
from swagger_server.src.tools.tools import (
    get_families_base_path,
    get_my_family_id,
    get_fam,
    get_fam_path,
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
            # load active env on startup
            # initial_activate_env()

            self.__family_controller_list = []
            self.__max_length = 3
            self.__my_family_id = self.get_my_family_id()
            self.__family_controller_list.append(
                FamilyController(id=self.__my_family_id)
            )
            BackEndController.__instance = self

    def add_family(self, family_name):
        """add_environment

        Just a testfunction to test the families list.


        :rtype: Str
        """
        new_fam = FamilyController(family_name)
        if len(self.__family_controller_list) >= self.__max_length:
            self.__family_controller_list.pop()
        self.__family_controller_list.insert(1, new_fam)
        return f"This is the new added family {new_fam.getName()}"

    def get_families_lists(self):
        """get_environments_lists

        Returns the environment ID of the environment from the environment_controller.


        :rtype: Str
        """
        fam_list_string = "List: "
        if not self.__family_controller_list:
            return "Families list is empty"
        for fam in self.__family_controller_list:
            fam_list_string += f"{fam.getID()}, "
        return fam_list_string

    def get_family_index_from_list(self, family_id):
        """get_environment_index_from_list

        Search for a controller in the environment_controller list for a specific ID.
        If nothings match, it returns None


        :rtype: int
        """
        for index, controller in enumerate(self.__family_controller_list):
            if controller.getID() == family_id:
                return index
        return None

    def get_families(self):
        """get_environments

        List all available environment ids


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
        """get_environments_environment_id

        Get the information for one environment

        :param environment_id:
        :type environment_id: str

        :rtype: Environment
        """
        check_uuid(family_id)

        return get_fam(family_id)

    def get_family_controller(self, family_id):
        """get_environment_controller

        Method for testing: Returns the environment_controller for a given ID


        :rtype: EnvironmentController
        """
        for fam in self.__family_controller_list:
            if str(fam.getID()) == family_id:
                print(f"EnvController id: {fam.getID()}")
                return fam
        return None

    def get_my_family_id(self):
        my_family_marker = os.path.join(get_families_base_path(), "my_family")
        with open(my_family_marker) as f:
            lines = f.readlines()
        return lines[0].split()[0]

    # def get_env_base_path(self):
    #     """get_environments

    #     List all available environment ids


    #     :rtype: List[Environment]
    #     """
    #     p = BackendConfig.base_env_path
    #     if not os.path.exists(p):
    #         os.mkdir(p)
    #     return p

    def set_my_family(self, family_id):
        """set_active_env

        Set the active environment.


        :rtype: Environment
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
        """update_active_env_marker

        Update the active_env file with the new ID.


        :rtype: None
        """
        self.my_family_delete()
        fam_path = get_fam_path(family_id)
        if not (os.path.exists(fam_path)):
            err_msg = f"Environment not found. {fam_path} folder does not exist"
            log.error(err_msg)
            raise NotFound(err_msg)
        my_family_marker = os.path.join(get_families_base_path(), "my_family")
        with open(my_family_marker, "w") as f:
            f.writelines(family_id)

    def my_family_get(self):
        """active_env_get

        Returns the active Environment.


        :rtype: Environment
        """
        try:
            name = get_my_family_id()
        except FileNotFoundError:
            err_msg = "No active environment set"
            log.error(err_msg)
            raise NotFound(err_msg)
        return get_fam(name)

    def my_family_delete(self):
        """active_env_delete

        Removes active_env marker/file.


        :rtype: Str, HTML_code
        """
        my_family_marker = os.path.join(get_families_base_path(), "my_family")
        if not os.path.exists(my_family_marker):
            return "OK", 200

        os.remove(my_family_marker)
        return "OK", 200
