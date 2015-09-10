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
        return {'redirect': request.POST['came_from'], 'success': True}

To be precise, the route name is the option 'pyramid.route_name', and
verify_login is
:py:func:`pyramid_persona.views.verify_login`. `request.POST['came_from']`
is the url of the page on which the button was clicked ; by default we
redirect the user back there after the login. The `success` value in
the response tells the javascript side whether the login was
successful: it is needed to make sure the user stays logged-out for
Persona.

So, if you want to check that an email is on a whitelist, create a profile and
redirect new users, you can define a new login view like this one::

    @view_config(route_name='login', check_csrf=True, renderer='json')
    def login(request):
        email = verify_login('email')
        if email not in whitelist:
            request.session.flash('Sorry, you are not on the list')
            return {'redirect': '/', 'success': False}
    request.response.headers.extend(remember(request, email))
        if not exists_in_db(email):
            create_profile(email)
            return {'redirect': '/new-user', 'success': True}
        return {'redirect': '/welcome-again', 'success': True}

Same goes if you want to do extra stuff at logout. The default logout view looks like this::

    @view_config(route_name='logout', check_csrf=True, renderer='json')
    def logout(request):
        request.response.headers.extend(forget(request))
        return {'redirect': request.POST['came_from']}


Override the default forbidden view
===================================

`pyramid_persona` provides a default view for rendering the 403 forbidden
response to non-authenticated users but you can override this view if you wish
with pyramid's `forbidden_view_config` decorator.

If you simply want to use a different template of your own design::

    from pyramid.renderers import render_to_response

    @forbidden_view_config()
    def forbidden(request):
        response = render_to_response('templates/403.pt',
                                     {'js': request.persona_js, 'button': request.persona_button},
                                     request=request)
        response.status_int = 403
        return response


You could also override the forbidden view to change the behaviour depending
on whether or not a user is authenticated. In this example authenticated users
are shown the permission denied view while non-authenticated users are
redirected to the login page::

    @forbidden_view_config(renderer='403.jinja2')
    def forbidden(request):
        if authenticated_userid(request):
            request.response.status = 403
            return {}
        url = request.route_url('login_form_view',
                                _query={request.registry['persona.redirect_url_parameter']: request.path})
        return HTTPSeeOther(url)


Note that `pyramid_persona` doesn't provide a login view that responds to GET
requests and so for the above to work would require you to create and register
an appropriate login view that renders the GET version of the login page.

In order to enable the user to return to the page they were attempting to view
once they have successfully authenticated `pyramid_persona` adds a parameter
to the querystring indicate where to redirect to. This value defaults to
`came_from` and so the in the above example the non-authenticated user would
be redirected to /login?came_from=<name of page attempted to view> (assuming
of course that the user has add a login page at /login). The name of the
parameter used in the querystring is configurable via the
`persona.redirect_url_parameter` setting.


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
  `SignedCookieSessionFactory`. You can override it if you prefer.
- it adds a `persona_js` request attribute containing the javascript code needed to make persona work.
- it adds a `persona_button` request attribute containing html code for quickly putting a login button.
- it defines the `/login` and `/logout` views to handle the persona workflow.
- it defines a basic forbidden view with a login button.

You can replace any part you like if the default behaviour doesn't
work for you and the configuration isn't enough.
