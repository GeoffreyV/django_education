from django.contrib import admin
from django.conf import settings
from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static

from .views import index, upload_eleves,\
    lister_ressources_si, afficher_sequence_si, lister_ressources_info, afficher_sequence_info, lister_competences,\
    afficher_famille_competence,  afficher_competence, chart, relative_url_view, relative_url_view_systeme,\
    lister_systemes, resultats, resultats_vierge, details, ds_eleve, resultats_quizz, contact, thanks, afficher_systeme

app_name = 'registration'
urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^password-change-done/$',
        auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
        name='password_change_done'
    ),
    url(r'^password-change/$',
        auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
        name='password_change'
    ),
    path('si/<int:id_sequence>/', afficher_sequence_si),
    path('info/<int:id_sequence>/', afficher_sequence_info),
    url('^si/', lister_ressources_si),
    url('^info/', lister_ressources_info),
    url('^competences', lister_competences),
    url('^systemes', lister_systemes),
    path('systeme/<int:id_systeme>/', afficher_systeme),
    path('competence/<int:id_famille>/', afficher_famille_competence),
    path('competence/<int:id_famille>/<int:id_competence>/', afficher_competence),
    path('q/<str:nomquiz>/<str:action>/uploads/<str:year>/<str:month>/<str:day>/<str:nom>.<str:ext>', relative_url_view),
    path('admin/django_education/systeme/<str:id_systeme>/<str:action>/systemes/<str:nom>.<str:ext>', relative_url_view_systeme),
    path('admin/multichoice/mcquestion/<str:nomquiz>/<str:action>/uploads/<str:year>/<str:month>/<str:day>/<str:nom>.<str:ext>', relative_url_view),
    path('resultats/<int:id_etudiant>/ds/', ds_eleve),
    path('resultats/<int:id_etudiant>/details/', details),
    url('^resultats/details/', details),
    path('resultats/<int:id_etudiant>/', resultats),
    url('^resultats/', resultats_vierge),
    url('^resultats_quizz/', resultats_quizz),
    url('^jchart',chart),
    url(r'^q/', include('quiz.urls')),
    url('^upload_eleves/$', upload_eleves),
    url('^contact/$', contact),
    url('^thanks/$', thanks),
    url('^$', index),
    path('admin/', admin.site.urls)
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
