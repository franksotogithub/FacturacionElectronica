from django.urls import reverse
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from usuarios.models import Usuario ,Permiso
from modulos.models import Menu


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

def permission(func):
    def wrapper(*args, **kwargs):
        request = args[0]
        url_login = reverse('usuarios:login')

        if not request.user.is_authenticated:
            if url_login != request.path:
                url_redirect = '?next='.join((url_login, request.path),)
                return redirect(url_redirect)
        else:
            string_url='{}'.format(request.path)
            array=string_url.split('/')

            slug_consult=array[-2]
            slug_consult2 = array[-1]
            if slug_consult2!='':
                slug_consult=slug_consult2
            menux = Usuario.objects.get(id=request.user.id).rol.permiso_set.values('menu_id')
            cant_match = Menu.objects.filter(id__in=menux,slug=slug_consult, estado=True).count()
            #cant_match=menu.filter(slug=slug_consult).count()
            #print ('cant_match-->',cant_match)
            #print('slug-->', slug_consult)

            if cant_match>0:
                if url_login == request.path:
                    return redirect(reverse('facturacion:facturas'))
            else:
                raise PermissionDenied
        return func(*args, **kwargs)
    return wrapper