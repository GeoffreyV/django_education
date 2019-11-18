from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin
from .models import sequence, filiere_prepa, ecole, concours, sujet, systeme, cours, td, tp, matiere, langue_vivante,\
    Etudiant, Professeur, Utilisateur, cours_info, td_info, tp_info, competence, khole, DS, Note, parametre,\
    grandeur, type_de_fichier, type_image_systeme, fichier_systeme, image_systeme

class ParametreInline(admin.TabularInline):
    model=parametre

class FichierInline(admin.TabularInline):
    model=fichier_systeme

class ImageInline(admin.TabularInline):
    model=image_systeme


class SystemeAdmin(admin.ModelAdmin):
    inlines=[
        ParametreInline,
        FichierInline,
        ImageInline
    ]

admin.site.register(sequence)
admin.site.register(filiere_prepa)
admin.site.register(ecole)
admin.site.register(concours)
admin.site.register(sujet)
admin.site.register(grandeur)
admin.site.register(type_de_fichier)
admin.site.register(type_image_systeme)
admin.site.register(systeme, SystemeAdmin)
admin.site.register(td)
admin.site.register(tp)
admin.site.register(cours_info)
admin.site.register(td_info)
admin.site.register(tp_info)
admin.site.register(matiere)
admin.site.register(langue_vivante)
admin.site.register(Utilisateur)
admin.site.register(Etudiant)
admin.site.register(Professeur)
admin.site.register(cours)
admin.site.register(competence)
admin.site.register(khole)
admin.site.register(DS)
admin.site.register(Note)
