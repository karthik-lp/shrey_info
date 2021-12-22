from uuid import uuid4
import logging


log = logging.getLogger("swagger_server.members_controller")


class MembersController:
    __members = None
    __id = None

    def __init__(self, members=None):
        if members:
            self.__members = members
        self.__id = uuid4()
        self.__members = ["member_1"]
        # Load the members controller

    @classmethod
    def get(self):
        return "Im the members controller."

    def getMembers(self):
        return self.__members

    def addMember(self, member_name):
        self.__members.append(member_name)
        return f"Successfully added the new Member {member_name} to the Members list"

    def getID(self):
        return self.__id
