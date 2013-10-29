from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.request import Request

from velruse.api import login_url
from velruse.app import find_providers

from kotti_velruse import log, _
from kotti_velruse.events import before_kotti_velruse_loggedin, before_kotti_velruse_loggedout, \
                                 after_kotti_velruse_loggedin,  after_kotti_velruse_loggedout


def login(request):
    settings = request.registry.settings
    try:
        #TODO:: before_kotti_velruse_loggedin(request)
        return {
            'project' : settings['kotti.site_title'],
            'login_url': request.route_url('login_'),
        }
    except Exception as e:
        log.error(e.message)
        raise HTTPNotFound(e.message).exception


def login_(request):
    ######################################################################################
    #                                                                                    #
    # Let's clarify the difference between "provider" and "method" in this function:     #
    #                                                                                    #
    # * Conceptually, [authentication] methods can be understood pretty much like        #
    #   protocols or transports. So, methods would be for example: OpenID, OAuth2 and    #
    #   other authentication protocols supported by Velruse.                             #
    #                                                                                    #
    # * A provider is simply an entity, like Google, Yahoo, Twitter, Facebook, Verisign, #
    #   Github, Launchpad and hundreds of other entities which employ authentication     #
    #   methods like OpenID, OAuth2 and others supported by Velruse.                     #
    #                                                                                    #
    # * In particular, certain entities implement their own authentication methods or    #
    #   they eventually offer several authentication methods. For this reason, there are #
    #   specific methods for "yahoo", "tweeter", "google_hybrid", "google_oauth2", etc.  #
    #                                                                                    #
    ######################################################################################

    provider = request.params['provider']
    method = request.params['method']

    settings = request.registry.settings
    if not method in find_providers(settings):
        raise HTTPNotFound('Provider {}({}) is not configured'.format(provider, method)).exception

    velruse_url = login_url(request, method)

    payload = dict(request.params)
    if 'yahoo'    == method: payload['oauth'] = 'true'
    if 'openid'   == method: payload['use_popup'] = 'false'
    payload['format'] = 'json'
    del payload['provider']
    del payload['method']

    redirect = Request.blank(velruse_url, POST=payload)
    try:
        before_kotti_velruse_loggedin(request, payload)
        response = request.invoke_subrequest( redirect )
        return response
    except Exception as e:
        log.error(e.message)
        message = _(u'Provider:{} Method:{} :: {}').format(provider, method, e.message)
        raise HTTPNotFound(message).exception



def logged_in(request):
    token = request.params['token']
    storage = request.registry.velruse_store
    try:
        json = storage.retrieve(token)
        after_kotti_velruse_loggedin(request, json)
        return json
    except Exception as e:
        log.error(e.message)
        provider='?'
        method='?'
        message = _(u'Provider:{} Method:{} :: {}').format(provider, method, e.message)
        raise HTTPNotFound(message).exception


def logout(request):
    from pyramid.security import forget
    try:
        before_kotti_velruse_loggedout(request)
        request.session.invalidate()
        request.session.flash( _(u'Session logged out.') )
        headers = forget(request)
        after_kotti_velruse_loggedout()
        return HTTPFound(location=request.application_url, headers=headers)
    except Exception as e:
        log.error(e.message)
        raise HTTPNotFound(e.message).exception
