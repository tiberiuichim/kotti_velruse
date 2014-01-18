import sys

from pprint import pformat

from velruse.api import login_url
from velruse.app import find_providers

from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPNotFound
from pyramid.request import Request
from pyramid.security import remember

from kotti.util import _
from kotti.views.util import is_root

from kotti_velruse import log
from kotti_velruse.events import AfterLoggedInObject
from kotti_velruse.events import after_kotti_velruse_loggedin



def includeme(config):
    includeme_views(config)
    includeme_override_views(config)
    includeme_static_views(config)
    log.info('{} configured'.format(__name__))


def includeme_views(config):
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

    config.add_route('login',     '/login')
    config.add_route('logged_in', '/logged_in')


def includeme_override_views(config):
    # override @@login
    config.add_view(name='login',
                    view=login_select,
                    custom_predicates=( is_root, ),
                    renderer='kotti_velruse:templates/login.mako')


def includeme_static_views(config):
    try:
        import openid_selector
        config.add_static_view(name='js',     path='openid_selector:/js')
        config.add_static_view(name='css',    path='openid_selector:/css')
        config.add_static_view(name='images', path='openid_selector:/images')
        log.info(_(u'openid_selector loaded successfully'))
    except Exception as e:
        log.exception(_(u'Failure loading openid-selector.\nStacktrace follows:\n{}').format(e))
        raise e



def login_select(context, request):
    log.debug( sys._getframe().f_code.co_name )
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
    import pdb; pdb.set_trace()
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

    log.debug( sys._getframe().f_code.co_name )

    ####################################################################################
    #TODO: should pass "came_from" to view "logged_in" so that we can redirect
    #      to the previous page. Sorry... I failed to make it work :(
    #-- came_from = request.params.get('came_from', request.resource_url(context))
    ####################################################################################

    provider = request.params['provider']
    method = request.params['method']

    settings = request.registry.settings
    if not method in find_providers(settings):
        raise HTTPNotFound('Provider/method {}/{} is not configured'.format(provider, method)).exception

    payload = dict(request.params)
    payload['format'] = 'json'
    if 'yahoo'  == method: payload['oauth'] = 'true'
    if 'openid' == method: payload['use_popup'] = 'false'
    del payload['provider']
    del payload['method']

    try:
        url = login_url(request, method)
        response = request.invoke_subrequest( Request.blank(url, POST=payload) )
        return response
    except Exception as e:
        message = _(u'Provider/method: {}/{} :: {}.').format(provider, method, e.message)
        log.exception(_(u'{}\nStacktrace follows:\n{}').format(message, e))
        raise HTTPNotFound(message).exception


def logged_in(context, request):
    """Velruse redirects to /logged_in when authentication succeeds"""

    log.debug( sys._getframe().f_code.co_name )

    ####################################################################################
    #TODO: should receive "came_from" somehow so that we can redirect to the previous
    #      page. Sorry... I failed to make it work :(
    #-- came_from = request.params.get('came_from', request.resource_url(context))
    ####################################################################################

    token = request.params['token']
    storage = request.registry.velruse_store
    json = None
    try:
        user = request.user
        json = storage.retrieve(token)
        obj = AfterLoggedInObject(json, user, request)
        after_kotti_velruse_loggedin(obj)
        principal = obj.principal
        identities = obj.identities
        if principal is None or identities is None:
            raise RuntimeError(_(u'Authentication events not being handled properly'))

        log.debug(_('User authenticated: id={}, name="{}", email="{}"').format(
            principal.id, principal.name, principal.email))
        headers = remember(request, principal.name)

        ###########################################################################################
        #TODO: at this point, we should actually redirect to the address which should be passed on
        #      variable "came_from". Because I failed to pass this variable around, I at least
        #      return to page @@prefs when user is not None.
        ###########################################################################################
        redirect = request.resource_url(context)
        if user is None:
            request.session.flash(
                _(u"Welcome, ${user}!", mapping=dict(user=principal.title or principal.name)), 'success')
        else:
            redirect += "@@prefs"

        log.debug('redirect to {} with headers = {}'.format(redirect, headers))
        return HTTPFound(location=redirect, headers=headers)
    except Exception as e:
        if json:
            log.exception(_(u'JSON received from provider: {}\nStacktrace follows:\n{}').format(json, e))
        else:
            log.exception(_("No JSON found in storage for token {}.\nStacktrace follows:\n{}").format(token, e))

        raise HTTPNotFound(e.message).exception
