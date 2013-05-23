Customization
-------------

Do extra work or verification at login
======================================

The default login view might not do exactly what you want. You might want to do
something when a new user logs for the first time, like create their profile in
the database, or redirect them to some page, or you might want to make additional
checks before logging them.

The easier way to do see is by overriding the login view. The default view is
defined like this::

    @view_config(route_name='login', check_csrf=True, renderer='json')
    def login(request):
        # Verify the assertion and get the email of the user
        email = verify_login(request)
        # Add the headers required to remember the user to the response
        request.response.headers.extend(remember(request, email))
        # Return a json message containing the address or path to redirect to.
        return {'redirect': request.POST['came_from']}

To be precise, the route name is the option 'pyramid.route_name', and
verify_login is :py:func:`pyramid_persona.views.verify_login`. `request.POST['came_from']` is the url of the page on
which the button was clicked ; by default we redirect the user back there after the login.

So, if you want to check that an email is on a whitelist, create a profile and
redirect new users, you can define a new login view like this one::

    @view_config(route_name='login', check_csrf=True, renderer='json')
    def login(request):
        email = verify_login('email')
        if email not in whitelist:
            request.session.flash('Sorry, you are not on the list')
            return {'redirect': '/'}
	request.response.headers.extend(emember(request, email))
        if not exists_in_db(email):
            create_profile(email)
            return {'redirect': '/new-user'}
        return {'redirect': '/welcome-again'}

Some goes if you want to do extra stuff at logout. The default logout view looks like this::

    @view_config(route_name='logout', check_csrf=True, renderer='json')
    def logout(request):
        request.response.headers.extend(forget(request))
        return {'redirect': request.POST['came_from']}

What pyramid_persona does
=========================

`pyramid_persona` *is* a login system. It replaces login forms and
views, and the need to handle passwords.

`pyramid_persona` *is not* an authentication policy. It only handles
the login process and requires an authentication policy to remember
the user between requests (`AuthTktAuthenticationPolicy` is used by
default).

Here is, in details, what including `pyramid_persona` does :

- it defines an authentication policy, an authorization policy, and a session factory     (this is needed for csrf
  protection, and is why we need a secret). Defaults are  `AuthTktAuthenticationPolicy`, `ACLAuthorizationPolicy` and
  `UnencryptedCookieSessionFactoryConfig`. You can override it if you prefer.
- it adds a `persona_js` request attribute containing the javascript code needed to make persona work.
- it adds a `persona_button` request attribute containing html code for quickly putting a login button.
- it defines the `/login` and `/logout` views to handle the persona workflow.
- it defines a basic forbidden view with a login button.

You can replace any part you like if the default behaviour doesn't
work for you and the configuration isn't enough.
