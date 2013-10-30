import os
from setuptools import setup, find_packages


version = '0.2'


here = os.path.abspath(os.path.dirname(__file__))
README  = open(os.path.join(here, 'README.rst')).read()
AUTHORS = open(os.path.join(here, 'AUTHORS.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

long_description = (
    README
    + '\n' +
    AUTHORS
    + '\n' +
    CHANGES
)

setup_requires = [
    'setuptools_git >= 1.0',
    ]

install_requires = [
    'Kotti',
    'rgomes-velruse',
    'openid-selector'
    ]


setup(name='kotti_velruse',
      version=version,
      description="Kotti authentication with Velruse: OpenID, OAuth2, Google, Yahoo, Live, Facebook, Twitter and others",
      long_description=long_description,
      classifiers=[
          "Programming Language :: Python",
          "Framework :: Pyramid",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
      ],
      keywords='pyramid kotti authentication velruse openid oauth2 google yahoo live facebook twitter',
      author='Richard Gomes',
      author_email='rgomes.info@gmail.com',
      url='http://kotti_velruse.readthedocs.org',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      setup_requires=setup_requires, 
      install_requires=install_requires,
      )
