from kotti.events import notify, ObjectEvent


class AfterKottiVelruseLoggedIn(ObjectEvent):
    """This event is emitted when a user logs in."""


def after_kotti_velruse_loggedin(userLoginObject):
    notify( AfterKottiVelruseLoggedIn(userLoginObject) )


class AfterLoggedInObject(object):
    def __init__(self, json, user=None, request=None):
        self.json = json
        self.user = user
        self.request = request
        self.principal = None
        self.identities = None
