from .models import systeme
import django_filters

class SystemeFiltre(django_filters.FilterSet):
    nom = django_filters.CharFilter(label='Nom du système',lookup_expr='icontains')

    class Meta:
        model = systeme
        fields = ['nom']
