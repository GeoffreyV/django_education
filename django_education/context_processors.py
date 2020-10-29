from .models import Menus, Matiere, ParametresGeneaux

def access_menus(request):
    """
        Definition of global menu
    """
    menus = Menus.objects.all()
    matieres = Matiere.objects.all()
    params_generaux = ParametresGeneaux.objects.first()

    return {'menus':menus, 'matieres':matieres, 'params_generaux':params_generaux}
