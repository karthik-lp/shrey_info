from swagger_server.controllers.backend_controller import BackEndController
from swagger_server.controllers.family_controller import FamilyController

"""Create Families service"""

method_decorators = []


def get():
    return FamilyController.get_families()


def post(friendly_name=""):
    return BackEndController.get_instance().add_family(friendly_name=friendly_name)


def search():
    # NOTE: we need to wrap it with list for Python 3 as dict_values is not JSON serializable
    return FamilyController.get_families()


def delete():
    return BackEndController.get_instance().delete_families()


def get(family_id):
    return BackEndController.get_instance().get_family(family_id)

