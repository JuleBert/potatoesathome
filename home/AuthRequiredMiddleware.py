import re

from django.shortcuts import redirect

from potatoesathome import settings

class AuthRequiredMiddleware(object):
    re_activate = re.compile('(activate|reset)/[A-Za-z]+/[0-9a-zA-Z\-]+')
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        auth_paths = [
            '/login/',
            '/signup/',
            '/loginandregister/',
            '/changePassword/',
            '/password_reset/',
            '/password_reset/done/',
            '/reset/done/',
        ]

        if request.path_info not in auth_paths and self.re_activate.search(request.path_info) is None:
            if not request.user.is_authenticated:
                return redirect('%s?next=%s' % (settings.LOGIN_path, request.path))

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        return response
