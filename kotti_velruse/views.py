from velruse.api import login_url
from velruse.app import find_providers

from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound
from pyramid.request import Request

from kotti.util import _

from kotti.views.login import logout
from kotti.views.login import forbidden_redirect
from kotti.views.login import forbidden_view
from kotti.views.login import forbidden_view_html

from kotti_velruse import log
from kotti_velruse.events import after_kotti_velruse_loggedin



def includeme(config):
    # wiring views from kotti.views.login
    config.add_route('logout',              '/logout')
    config.add_route('forbidden_redirect',  '/forbidden_redirect')
    config.add_route('forbidden_view',      '/forbidden_view')
    config.add_route('forbidden_view_html', '/forbidden_view_html')

    # views provided by this plugin
    config.add_view(login_select,
                    route_name='login',
                    request_method='GET',
                    renderer='kotti_velruse:templates/login.mako')
    config.add_view(login_verify,
                    route_name='login',
                    request_method='POST',
                    renderer='json')
    config.add_view(logged_in,
                    route_name='logged_in')
    config.add_view(logout,
                    route_name='logout',
                    permission='view')
    config.add_view(forbidden_redirect,
                    route_name='forbidden_redirect',
                    accept='text/html')
    config.add_view(forbidden_view,
                    route_name='forbidden_view')
    config.add_view(forbidden_view_html,
                    route_name='forbidden_view_html',
                    renderer='kotti:templates/forbidden.pt')

    config.add_route('login',     '/login')
    config.add_route('logged_in', '/logged_in')

    try:
        import openid_selector
        config.add_static_view(name='js',     path='openid_selector:/js')
        config.add_static_view(name='css',    path='openid_selector:/css')
        config.add_static_view(name='images', path='openid_selector:/images')
        log.info(_(u'openid_selector loaded successfully'))
    except Exception as e:
        log.exception(e)
        raise e
    log.info(_(u'kotti_velruse views are configured.'))
    

def login_select(context, request):
    came_from = request.params.get('came_from', request.resource_url(context))
    settings = request.registry.settings
    try:
        #TODO:: before_kotti_velruse_loggedin(request)
        return {
            'project' : settings['kotti.site_title'],
            'came_from': came_from,
            'login_url': request.route_url('login'),
        }
    except Exception as e:
        log.exception(e)
        raise HTTPNotFound(e.message).exception


def login_verify(context, request):
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
        raise HTTPNotFound('Provider/method {}/{} is not configured'.format(provider, method)).exception

    velruse_url = login_url(request, method)

    payload = dict(request.params)
    if 'yahoo'    == method: payload['oauth'] = 'true'
    if 'openid'   == method: payload['use_popup'] = 'false'
    payload['format'] = 'json'
    del payload['provider']
    del payload['method']

    redirect = Request.blank(velruse_url, POST=payload)
    try:
        response = request.invoke_subrequest( redirect )
        return response
    except Exception as e:
        log.exception(e)
        message = _(u'Provider/method: {}/{} :: {}').format(provider, method, e.message)
        raise HTTPNotFound(message).exception



from pyramid.security import remember


from kotti_velruse.events import AfterLoggedInObject


def logged_in(context, request):
    """Velruse automatically requests /logged_in when authentication succeeds"""
    came_from = request.params.get('came_from', request.resource_url(context))
    token = request.params['token']
    storage = request.registry.velruse_store
    try:
        json = storage.retrieve(token)
        obj = AfterLoggedInObject(json)
        after_kotti_velruse_loggedin(obj, request)
        print(obj.principal.id)
        print(obj.principal.name)
        print(obj.principal.email)
        headers = remember(request, str(obj.principal.id))
        request.session.flash(
            _(u"Welcome, ${user}!", mapping=dict(user=obj.principal.name)), 'success')
        return HTTPFound(location=came_from, headers=headers)
    except Exception as e:
        log.exception(e)
        raise HTTPNotFound(e.message).exception
