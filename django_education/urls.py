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
from django.urls import path
from django.conf.urls import url, include

from . import views

from .views import index, login, simple_upload, logout_view, lister_ressources, afficher_sequence, lister_competences, afficher_famille_competence,  afficher_competence, home
from jchart import views as jchart_views
from jchart.views import ChartView


#from .views import line_chart

urlpatterns = [
    url('^index$', index),
    url('^login$', login),
    url('^simple_upload$', simple_upload),
    url('^logout$', logout_view),
    url('^ressources', lister_ressources),
    url('^competences', lister_competences),
    url('^jharts',home),
    path('sequence/<int:id_sequence>/', afficher_sequence),
    path('competence/<int:id_famille>/', afficher_famille_competence),
    path('competence/<int:id_famille>/<int:id_competence>/', afficher_competence),
    url('^$', index),
    path('admin/', admin.site.urls),
]
