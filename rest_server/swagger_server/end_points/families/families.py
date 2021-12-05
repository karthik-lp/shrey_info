from swagger_server.controllers.backend_controller import BackEndController

"""Create Environment service"""

method_decorators = []
families = {}


def get():
    return BackEndController.get_instance().get_families()


def post(family_name=""):
    return BackEndController.get_instance().add_family(family_name=family_name)


def search():
    # NOTE: we need to wrap it with list for Python 3 as dict_values is not JSON serializable
    return BackEndController.get_instance().get_families()


def get(family_id):
    return f"environment view get id: {family_id}"
