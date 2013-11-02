from kotti.events import notify, ObjectEvent


class AfterKottiVelruseLoggedIn(ObjectEvent):
    """This event is emitted when a user logs in."""


def after_kotti_velruse_loggedin(userLoginObject, request):
    notify( AfterKottiVelruseLoggedIn(userLoginObject, request) )


class AfterLoggedInObject(object):
    def __init__(self, json):
        self.json = json
        self.principal = None
        self.identities = None
