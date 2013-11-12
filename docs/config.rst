Configuration
-------------

You can override any policy or view defined by `pyramid_persona` by defining them the usual way.

`pyramid_persona` defines the following settings :

persona.secret
    A secret string used to sign cookies. Required only if you do not defined another session factory.

persona.audiences
    The protocol, domain name, and port of your site, as defined in the `persona documentation`_. Can contain more than one value. Required.

persona.verifier
    The doted python name of the BrowserID assertion verifier. Optional. Default is 'browserid.RemoteVerifier'. Another possible value could be 'browserid.LocalVerifier' (not recommended for now).

persona.redirect_url_parameter
    The name of a querystring parameter which can be use to determine the url
    to redirect to after successful login e.g. example.com/login?came_from=/edit would redirect to example.com/edit. Optional, default is `came_from`.

.. _`persona documentation`: https://developer.mozilla.org/en-US/docs/Persona/Remote_Verification_API

Login dialog customization
++++++++++++++++++++++++++

Persona provides a few ways to customize the login dialog. To be precise, they
are arguments to the `navigator.id.request` API call. For the full description of these parameters,
see `the documentation of navigator.id.request`_.

.. _the documentation of navigator.id.request: https://developer.mozilla.org/en-US/docs/DOM/navigator.id.request

persona.siteName
    Plain text name of your site to show in the login dialog. Optional.

persona.siteLogo
    Absolute path to an image to show in the login dialog. Optional.

persona.privacyPolicy
    Absolute path or URL to the web site's privacy policy. Optional.

persona.termsOfService
    Absolute path or URL to the web site's terms of service. Optional.

persona.backgroundColor
    A hexadecimal color to use as the login dialog's background. Format: "#rgb" or "#rrggbb". Optional.

Routes
++++++

If the default route names or paths conflicts with your application, you can change them :

persona.login_route
    The login route name. Optional, default is 'login'.

persona.login_path
    The login route path. Optional, default is '/login'.

persona.logout_route
    The logout route name. Optional, default is 'logout'.

persona.logout_path
    The logout route path. Optional, default is '/logout'.
