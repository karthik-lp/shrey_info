from uuid import uuid4
from swagger_server.controllers.members_controller import MembersController


class FamilyController:
    __name = None
    __id = None
    __members_controller = None

    def __init__(self, name=None, id=None):
        self.__name = name
        if id:
            self.__id = id
        else:
            self.__id = uuid4()

        # Load the member controller
        self.__members_controller = MembersController()

    @classmethod
    def get(self):
        return "Im the family controller."

    def getName(self):
        return self.__name

    def getID(self):
        return self.__id

    def getMembersController(self):
        return self.__members_controller
