import threading

_user = threading.local()


class CurrentUserMiddleware:
    """Middleware para armazenar o usuário atual na thread local."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _user.value = request.user if request.user.is_authenticated else None
        response = self.get_response(request)
        return response


def get_current_user():
    """Retorna o usuário atual salvo na thread local."""
    return getattr(_user, 'value', None)
