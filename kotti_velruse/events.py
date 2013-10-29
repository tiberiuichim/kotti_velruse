from kotti.events import notify, ObjectEvent


class BeforeKottiVelruseLoggedIn(ObjectEvent):
    pass

class AfterKottiVelruseLoggedIn(ObjectEvent):
    pass

def before_kotti_velruse_loggedin(request, payload):
    notify( BeforeKottiVelruseLoggedIn(request, payload) )

def after_kotti_velruse_loggedin(request, json):
    notify( AfterKottiVelruseLoggedIn(request, json) )




class BeforeKottiVelruseLoggedOut(ObjectEvent):
    pass

class AfterKottiVelruseLoggedOut(ObjectEvent):
    pass

def before_kotti_velruse_loggedout(request):
    notify( BeforeKottiVelruseLoggedOut(request) )

def after_kotti_velruse_loggedout():
    notify( AfterKottiVelruseLoggedOut() )
