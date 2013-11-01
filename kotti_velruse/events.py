from kotti.events import notify, ObjectEvent


class AfterKottiVelruseLoggedIn(ObjectEvent):
    """This event is emitted when a user logs in."""


def after_kotti_velruse_loggedin(json, request):
    notify( AfterKottiVelruseLoggedIn(json, request) )
