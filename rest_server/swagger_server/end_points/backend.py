from swagger_server.controllers.backend_controller import BackEndController
# from connexion import NoContent


"""Create Backend service"""

method_decorators = []
backends = {}


def get():
    return BackEndController.get_instance().get_families_lists()


def search():
    # NOTE: we need to wrap it with list for Python 3 as dict_values is not JSON serializable
    return BackEndController.get_instance().get_families_lists()


# def delete():
#     return backend_error_codes.error_codes.BACK_END_ERROR_CODES["BACK00002"]
