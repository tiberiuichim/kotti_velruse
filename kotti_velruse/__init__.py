from pyramid.i18n import TranslationStringFactory


log = __import__('logging').getLogger(__name__)


_ = TranslationStringFactory('kotti_velruse')


def kotti_configure(settings):
    settings['pyramid.includes'] += ' velruse.app'
    settings['pyramid.includes'] += ' kotti_velruse'
    #-- settings['kotti.populators'] += ' kotti_velruse.populate.populate_settings'


def includeme(config):
    import views

    config.add_view(views.login,
                    route_name='login',
                    request_method='GET',
                    renderer='kotti_velruse:templates/login.mako')
    config.add_view(views.login_,
                    route_name='login_',
                    renderer='json')
    config.add_view(views.logged_in,
                    route_name='logged_in',
                    renderer='json')
    config.add_view(views.logout,
                    route_name='logout',
                    permission='view')

    config.add_route('login',     '/login')
    config.add_route('login_',    '/login_')
    config.add_route('logged_in', '/logged_in')
    config.add_route('logout',    '/logout')

    import openid_selector
    config.add_static_view(name='js',     path='openid_selector:/js')
    config.add_static_view(name='css',    path='openid_selector:/css')
    config.add_static_view(name='images', path='openid_selector:/images')
    
