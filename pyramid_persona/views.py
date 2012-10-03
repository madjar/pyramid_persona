import pkg_resources
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.response import Response
from pyramid.security import remember, forget

import browserid.errors


def _check_csrf_token(request):
    """Check the CSRF token from the request. Raises if invalid.

    Copied from pyramid.session.check_csrf_token in pyramid==1.4a2."""
    if request.params.get('csrf_token') != request.session.get_csrf_token():
        raise HTTPBadRequest('incorrect CSRF token')


def login(request):
    """View to check the persona assertion and remember the user"""
    _check_csrf_token(request)
    verifier = request.registry['persona.verifier']
    try:
        data = verifier.verify(request.POST['assertion'])
    except (ValueError, browserid.errors.TrustError):
        raise HTTPBadRequest('invalid assertion')
    headers = remember(request, data['email'])
    return Response(headers=headers)


def logout(request):
    """View to forget the user"""
    _check_csrf_token(request)
    headers = forget(request)
    return Response(headers=headers)


def forbidden(request):
    """A basic 403 view, with a login button"""
    template = pkg_resources.resource_string('pyramid_persona', 'templates/forbidden.html').decode()
    html = template % {'js': request.persona_js, 'button': request.persona_button}
    return Response(html, status='403 Forbidden')
