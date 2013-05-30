"""This is a demo app. It is basically the app that was presented
in http://compiletoi.net/quick-authentication-on-pyramid-with-persona.html.

To run it, you'll need pyramid, pyramid_persona and waitress.

The button integration example is a /.
The forbidden view example is at /restricted.
"""
from __future__ import print_function
import logging

from waitress import serve
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.security import authenticated_userid, remember
from pyramid.exceptions import Forbidden
from pyramid_persona.views import verify_login


def restricted(request):
    userid = authenticated_userid(request)
    if userid is None:
        raise Forbidden()
    return Response('Hello %s!' % (userid,))


def template(request):
    userid = authenticated_userid(request)
    return {'message': 'Hello', 'user': userid}


def first_time(request):
    userid = authenticated_userid(request)
    return {'message': 'Welcome', 'user': userid}


KNOWN = set()


@view_config(route_name='login', check_csrf=True, renderer='json')
def login(request):
    email = verify_login(request)
    if email == 'denied@mockmyid.com':
        return {'redirect': request.POST['came_from'], 'success': False}

    request.response.headers = remember(request, email)
    if email not in KNOWN:
        KNOWN.add(email)
        print(email, 'just logged in for the first time')
        return {'redirect': '/welcome', 'success': True}
    else:
        return {'redirect': request.POST['came_from'], 'success': True}


if __name__ == '__main__':
    settings = {
        'persona.secret': 'some secret',
        'persona.audiences': 'http://localhost:8080',
        'mako.directories': '.',
        'persona.siteName': 'Super demo app',
        'persona.privacyPolicy': '/nonExistentPrivacy.html',
        'persona.termsOfService': '/nonExistentTos.html',
    }
    logging.basicConfig(level=logging.DEBUG)
    config = Configurator(settings=settings)
    config.include('pyramid_persona')
    config.add_route('restricted', '/restricted')
    config.add_view(restricted, route_name='restricted')
    config.add_route('root', '/')
    config.add_view(template, route_name='root', renderer='hello.mako')
    config.add_route('first_time', '/welcome')
    config.add_view(first_time, route_name='first_time', renderer='hello.mako')
    config.scan('.')
    app = config.make_wsgi_app()
    serve(app, host='0.0.0.0')
