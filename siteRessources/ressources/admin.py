from django.contrib import admin
from .models import Matiere, Sequence, Competence, Famille_competence,\
Systeme, Ilot, Ressource, ParametresGeneaux
# Register your models here.


class RessourceAdmin(admin.ModelAdmin):
    def matiere(self,obj):
        return obj.sequence.matiere

    list_display = ('type', '__str__', 'matiere', 'sequence')
    list_filter = ['sequence__matiere', 'type']
    ordering = ['sequence__matiere', 'sequence', 'type' ]

admin.site.register(ParametresGeneaux)
admin.site.register(Famille_competence)
admin.site.register(Competence)
admin.site.register(Matiere)
admin.site.register(Sequence)
admin.site.register(Ressource, RessourceAdmin)
admin.site.register(Systeme)
admin.site.register(Ilot)
