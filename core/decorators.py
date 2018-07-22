from django.urls import reverse
from django.shortcuts import redirect


def logged(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        url_login = reverse('usuarios:login')
        print(url_login, request.path)
        if not request.user.is_authenticated:
            if url_login != request.path:
                url_redirect = '?next='.join((url_login, request.path),)
                return redirect(url_redirect)
        elif url_login == request.path:
            return redirect(reverse('facturacion:facturas'))
        return func(*args, **kwargs)
    return wrapper