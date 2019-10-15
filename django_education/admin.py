from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.contrib.auth.admin import UserAdmin
from .models import sequence, filiere_prepa, ecole, concours, sujet, systeme, cours, td, tp, matiere, langue_vivante,\
    Etudiant, Professeur, Utilisateur, cours_info, td_info, tp_info, competence, khole, DS, Note

admin.site.register(sequence)
admin.site.register(filiere_prepa)
admin.site.register(ecole)
admin.site.register(concours)
admin.site.register(sujet)
admin.site.register(systeme)
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
