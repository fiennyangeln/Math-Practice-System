from .constants import *
from webmodels.models import *
from django.shortcuts import render, redirect

def is_skip_auth(request):
    for url in SKIP_AUTH_URL:
        print ("in skip_auth"+request.path+ " " + url)
        if (request.path == url):
            print("is_skip_auth=True")
            return True
    return False

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        if not is_skip_auth(request):
            if request.user.is_authenticated:
                print("authenticated user")
                user_permission = UserPermission.objects.filter(owner=(request.user)).first()

                if (user_permission is not None):
                    print ("user_permission not none")
                    if user_permission.is_teacher and not request.path.startswith(TEACHERS_ACTION):
                        return redirect(BASE_URL)
            else:
                return redirect(BASE_URL)
        print("returnign response")
        return response
