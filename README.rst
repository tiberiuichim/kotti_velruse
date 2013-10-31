
kotti_velruse
=============

| Code_ | Bugs_ | Forum_ | License_ | Contact_

.. _Code : http://github.com/frgomes/kotti_velruse
.. _Bugs : http://github.com/frgomes/kotti_velruse/issues
.. _Forum : http://github.com/frgomes/kotti_velruse/wiki
.. _License : http://opensource.org/licenses/BSD-3-Clause
.. _Contact : http://github.com/~frgomes


kotti_velruse is a `Kotti`_ plugin which provides authentication via `Velruse`_, using
methods such as: OpenID, OAuth2, Google, Yahoo, Live, Facebook, Twitter and others

.. _`Kotti`: http://kotti.readthedocs.org
.. _`Velruse`: http://velruse.readthedocs.org


Configuration
-------------

1. Insert *kotti_velruse.kotti_configure_ on *kotti.configurators* 

    kotti.configurators = kotti_tinymce.kotti_configure
                          kotti_velruse.kotti_configure


2. Insert the block below under section [app:main]

::

    ### --------------------------------------------------------------------------
    # velruse configuration
    #
    # Module velruse.app.includeme looks for entries named "provider." in order
    # to discover which providers are configured. 
    #
    # NOTE: these configurations must be inside [app:kotti]
    #
    ###
    
    
    #---
    # Please adjust variable REALM
    #
    # Make sure that:
    #
    #   1. your browser is able to resolve the FQDN
    #   2. your Kotti server is able to resolve the FQDN
    #
    #---
    realm=http://www.example.com
    
    
    endpoint = %(realm)s:6543/logged_in
    store = memory
    # store = redis
    # store.host = localhost
    # store.port = 6379
    # store.db = 0
    # store.key_prefix = velruse_ustore
    
    
    # OpenID
    #   Despite a single provide.openid is declared, you can specify multiple
    #   URLs that should be used for connecting to multiple OpenID endpoints.
    #   See: login.mako for an example of how this can be done
    provider.openid.realm=%(realm)s
    provider.openid.store=openid.store.memstore:MemoryStore
    
    # Google (this an alias to Google Hybrid, for backward compatibility)
    provider.google.realm=%(realm)s
    provider.google.consumer_key=CHANGE-ME
    provider.google.consumer_secret=CHANGE-ME
    provider.google.scope=CHANGE-ME
    
    # Google Hybrid
    #provider.google_hybrid.realm=%(realm)s
    #provider.google_hybrid.consumer_key=CHANGE-ME
    #provider.google_hybrid.consumer_secret=CHANGE-ME
    #provider.google_hybrid.scope=CHANGE-ME
    
    # Google OAuth2
    provider.google_oauth2.consumer_key=CHANGE-ME
    provider.google_oauth2.consumer_secret=CHANGE-ME
    provider.google_oauth2.scope=CHANGE-ME
    
    # Yahoo
    provider.yahoo.realm=%(realm)s
    provider.yahoo.consumer_key=CHANGE-ME
    provider.yahoo.consumer_secret=CHANGE-ME
    
    # Live
    provider.live.client_id=CHANGE-ME
    provider.live.client_secret=CHANGE-ME
    provider.live.consumer_key=CHANGE-ME
    provider.live.consumer_secret=CHANGE-ME
    
    # Twitter
    provider.twitter.consumer_key=CHANGE-ME
    provider.twitter.consumer_secret=CHANGE-ME
    
    # Facebook
    provider.facebook.app_id=CHANGE-ME
    provider.facebook.app_secret=CHANGE-ME
    provider.facebook.consumer_key=CHANGE-ME
    provider.facebook.consumer_secret=CHANGE-ME
    provider.facebook.scope=email,publish_stream,read_stream,create_event,offline_access
    
    # LinkedIn
    provider.linkedin.consumer_key=CHANGE-ME
    provider.linkedin.consumer_secret=CHANGE-ME
    
    # Github
    provider.github.consumer_key=CHANGE-ME
    provider.github.consumer_secret=CHANGE-ME
    provider.github.scope=CHANGE-ME
    
    # BitBucket
    provider.bitbucket.consumer_key=CHANGE-ME
    provider.bitbucket.consumer_secret=CHANGE-ME
    
    # MailRU
    provider.mailru.app_id=CHANGE-ME
    provider.mailru.app_secret=CHANGE-ME
    provider.mailru.consumer_key=CHANGE-ME
    provider.mailru.consumer_secret=CHANGE-ME
    
    ### --------------------------------------------------------------------------


3. Please adjust variable *realm* in development.ini.

4. Adjust provider configurations accordingly to to your affiliation keys and
   passwords.

.. note:: Several providers work out of the box, like Google Hybrid, Yahoo and most
          OpenID providers.

5. Navigate to page /login like shown below:

    $ firefox http://localhost:6543/login


Dependencies
------------

This plugin depends on modified versions of:

* velruse: https://github.com/frgomes/velruse/tree/feature.kotti_auth

* openid-selector: https://github.com/frgomes/velruse
