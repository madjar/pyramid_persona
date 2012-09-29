import browserid
import pkg_resources
from pyramid.response import Response
from pyramid.security import remember, forget


def login(request):
    """View to check the persona assertion and remember the user"""
    data = browserid.verify(request.POST['assertion'], request.registry.settings['persona.audience'])
    headers = remember(request, data['email'])
    return Response(headers=headers)


def logout(request):
    """View to forget the user"""
    headers = forget(request)
    return Response(headers=headers)


def forbidden(request):
    """A basic 403 view, with a login button"""
    template = pkg_resources.resource_string('pyramid_persona', 'templates/forbidden.html')
    html = template % {'js': request.persona_js, 'button': request.persona_button}
    return Response(html, status='403 Forbidden')
