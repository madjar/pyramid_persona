pyramid_persona
===============

`pyramid_persona` let you quickly set up authentication using persona_
on your pyramid_ project. It provides a way to conveniently replace
the login form and all the processing and security concerns that comes
with it. It aims at giving as much as possible with as little
configuration as possible, while still letting you customize if you
want. If you want to see some screenshots of the demo app, take a look
at this `blog post`_.

You can find it on pypi_ as `pyramid_persona`. Also don't forget to check the documentation_.

.. _persona: https://login.persona.org/
.. _pyramid: http://www.pylonsproject.org/
.. _pypi: http://pypi.python.org/pypi/pyramid_persona
.. _`blog post`: http://compiletoi.net/quick-authentication-on-pyramid-with-persona.html
.. _documentation: https://pyramid_persona.readthedocs.org/en/latest/

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

`pyramid_persona` *is* a login system. It replaces login forms and
views, and the need to handle passwords.

`pyramid_persona` *is not* an authentication policy. It only handles
the login process and requires an authentication policy to remember
the user between requests (`SessionAuthenticationPolicy` is used by
default).

Here is, in details, what including `pyramid_persona` does :

- it defines an authentication policy, an authorization policy, and a session factory     (this is needed for csrf
  protection, and is why we need a secret). Defaults are  `SessionAuthenticationPolicy`, `ACLAuthorizationPolicy` and
  `UnencryptedCookieSessionFactoryConfig`. You can override it if you prefer.
- it adds a `persona_js` request attribute containing the javascript code needed to make persona work.
- it adds a `persona_button` request attribute containing html code for quickly putting a login button.
- it defines the `/login` and `/logout` views to handle the persona workflow.
- it defines a basic forbidden view with a login button.

You can replace any part you like if the default behaviour doesn't
work for you and the configuration isn't enough.

Contact
-------

This project is made by Georges Dubus (`@georgesdubus`_). Bug reports and pull requests are welcome.

.. _`@georgesdubus`: https://twitter.com/georgesdubus
