from swagger_server.controllers.backend_controller import BackEndController

"""Create Zone service"""

method_decorators = []


def get():
    return "get active_env not implemented"


def post(body):
    back_end_controller = BackEndController.get_instance()
    return back_end_controller.set_my_family(body)


def search():
    return "get active_env not implemented"
