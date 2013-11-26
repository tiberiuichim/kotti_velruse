__version__ = '0.3.4'


log = __import__('logging').getLogger(__name__)


def kotti_configure(settings):
    settings['pyramid.includes'] += ' velruse.app'
    settings['pyramid.includes'] += ' kotti_velruse.views'
