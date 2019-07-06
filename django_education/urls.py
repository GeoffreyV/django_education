"""costadoat_education URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url, include
from django.views.generic import RedirectView

from .views import index, login, simple_upload, logout_view,\
    lister_ressources, afficher_sequence, lister_competences, afficher_famille_competence,  afficher_competence, chart,\
    compte, mes_quizzes, mes_ds, quizzes_etudiants, documents, gestion_ds, relative_url_view

urlpatterns = [
    url('^index$', index),
    url('^login$', login),
    url('^logout$', logout_view),
    url('^ressources', lister_ressources),
    path('sequence/<int:id_sequence>/', afficher_sequence),
    url('^competences', lister_competences),
    path('competence/<int:id_famille>/', afficher_famille_competence),
    path('competence/<int:id_famille>/<int:id_competence>/', afficher_competence),
    url('^compte$', compte),
    url('^q/quizz01/take/uploads/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/(?P<nom>[\w-]+).(?P<ext>[\w-]+)', relative_url_view),
    url('^mes_quizzes/', mes_quizzes),
    url('^mes_ds/', mes_ds),
    url('^quizzes_etudiants/', quizzes_etudiants),
    url('^documents/', documents),
    url('^gestion_ds/', gestion_ds),
    url('^jharts',chart),
    url(r'^q/', include('quiz.urls')),
    url('^simple_upload$', simple_upload),
    url('^$', index),
    path('admin/', admin.site.urls)
]
