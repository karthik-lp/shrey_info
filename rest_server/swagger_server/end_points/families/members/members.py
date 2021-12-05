from swagger_server.controllers.backend_controller import BackEndController

"""Create Zone service"""

method_decorators = []
members = {}


def get(family_id):
    fam_controller = BackEndController.get_instance().get_family(family_id)
    member_controller = fam_controller.getMemberController()
    return f"Member controller ID: {member_controller.getID()} Member List:{member_controller.getMembers()}"


def patch(family_id, member_id):
    fam_controller = BackEndController.get_instance().get_family(family_id)
    member_controller = fam_controller.getZoneController()
    member_controller.addZone(member_id)
    return f"Added member: {member_id}"


def search(family_id):
    fam_controller = BackEndController.get_instance().get_family(family_id)
    member_controller = fam_controller.getMemberController()
    return f"Zone controller ID: {member_controller.getID()} Zone List:{member_controller.getMembers()}"
