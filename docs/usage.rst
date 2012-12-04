Usage
=====

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