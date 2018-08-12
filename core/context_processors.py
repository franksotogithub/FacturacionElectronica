from modulos.models import Menu
from usuarios.models import Usuario


def menu(request):

    if request.user.is_authenticated:
        menux=Usuario.objects.get(id=request.user.id).rol.permiso_set.values('menu_id')
        menu=Menu.objects.filter(id__in=menux,estado=True)
    else:
        menu=Menu.objects.filter(requiere_autenticacion=False)

    return {"menu_page": {
        'website': menu,
        'sistema': []
        }
    }