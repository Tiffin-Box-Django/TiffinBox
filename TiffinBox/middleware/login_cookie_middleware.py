from django.contrib.auth.models import AnonymousUser


class LoginCookieMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not isinstance(request.user, AnonymousUser):
            if "uname" not in request.COOKIES:
                if request.user.is_authenticated:
                    response.set_cookie("ufname", request.user.first_name)
                    response.set_cookie("uname", request.user.username)
                    response.set_cookie("utype", request.user.client_type)
            else:
                if request.COOKIES["uname"] != request.user.first_name:
                    response.set_cookie("ufname", request.user.first_name)
                    response.set_cookie("uname", request.user.username)
                    response.set_cookie("utype", request.user.client_type)
        return response
