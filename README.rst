pyramid_persona
===============

`pyramid_persona` let you quickly set up authentication using persona_ on your pyramid_ project. It aims at giving as
much as possible with as little configuration as possible, while still letting you customize if you want. If you want to see some screenshots of the demo app, take a look at this `blog post`_.

You can find it on pypi_ as `pyramid_persona`.

.. _persona: https://login.persona.org/
.. _pyramid: http://www.pylonsproject.org/
.. _pypi: http://pypi.python.org/pypi/pyramid_persona
.. _`blog post`: http://compiletoi.net/quick-authentication-on-pyramid-with-persona.html

Very basic usage
----------------

First of all, include `pyramid_persona`. Add this in your project configuration ::

    config.include("pyramid_persona")

Then, we need two little lines in your config files : a secret used to sign cookies, and the audience,
the hostname and port of your website (this is needed for security reasons)::

    persona.secret = This is some secret string
    persona.audiences = http://localhost:6543

There, we're done. We now have a nice forbidden view with a persona login button.

Less basic usage
----------------

`pyramid_persona` also provides you a way to easily put a login or logout button on your pages. To do so, you need to
include jquery, the persona library, and some application-specific in your heads. The application specific javascript
can be accessed as `request.persona_js`.

Then, you can add the button in your page. `request.persona_button` provides a login if the user is not logged in, and
a logout button if they are.

A basic page might be (using mako) ::

    <html>
    <head>
        <script type="text/javascript" src="//ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
        <script src="https://login.persona.org/include.js" type="text/javascript"></script>
        <script type="text/javascript">${request.persona_js}</script>
    </head>
    <body>
    Hello ${user}
    ${request.persona_button}
    </body>
    </html>

Customized buttons
------------------

You can also use your own buttons. For that, you have to include the javascript like in the previous section and give
your login and logout button the `signin` and `signout` classes. For example ::

    <button id='signin'>login</button>
    <button id='signout'>logout</button>

What it does
------------

Here is, in details, what including `pyramid_persona` does :

- it defines an authentication policy, an authorization policy, and a session factory     (this is needed for csrf
  protection, and is why we need a secret). Defaults are  `SessionAuthenticationPolicy`, `ACLAuthorizationPolicy` and
  `UnencryptedCookieSessionFactoryConfig`. You can override it if you prefer.
- it adds a `persona_js` request attribute containing the javascript code needed to make persona work.
- it adds a `persona_button` request attribute containing html code for quickly putting a login button.
- it defines the `/login` and `/logout` views to handle the persona workflow.
- it defines a basic forbidden view with a login button.

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

Contact
-------

This project is made by Georges Dubus (`@georgesdubus`_). Bug reports and pull requests are welcome.

.. _`@georgesdubus`: https://twitter.com/georgesdubus
