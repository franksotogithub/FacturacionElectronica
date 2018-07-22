from modulos.models import Menu
def menu(request):
    return {"menu_page": {
        'website': Menu.objects.filter(),
        'sistema': []
        }
    }