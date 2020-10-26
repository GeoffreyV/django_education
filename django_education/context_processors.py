from .models import Menus

def access_menus(request):
    """
        Definition of global menu
    """
    menus = Menus.objects.all()
    return {'menus':menus}
