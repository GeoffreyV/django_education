from .models import Matiere, ParametresGeneaux

def ressource_renderer(request):
    return {'matieres':Matiere.objects.all()}
