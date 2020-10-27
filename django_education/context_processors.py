from .models import Menus, Matiere

def access_menus(request):
    """
        Definition of global menu
    """
    menus = Menus.objects.all()
    matieres = Matiere.objects.all()

    return {'menus':menus, 'matieres':matieres}
