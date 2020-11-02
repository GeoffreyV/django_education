from django.db import models
from .pedagogie import Matiere

class Filiere(models.Model):
    sigle=models.CharField(max_length=30)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return str(self.sigle)

    class Meta:
            ordering = ['id']


class Ecole(models.Model):
    sigle=models.CharField(max_length=30)
    nom = models.CharField(max_length=100)


class Concours(models.Model):
    filiere = models.ForeignKey('Filiere', on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom+' ('+str(self.filiere)+')'

    class Meta:
            ordering = ['nom']

class Grandeur(models.Model):
    nom = models.CharField(max_length=100)
    unite = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class parametre(models.Model):
    grandeur = models.ForeignKey('Grandeur', on_delete=models.CASCADE)
    valeur = models.FloatField()
    systeme = models.ForeignKey('Systeme', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.systeme)+' ('+str(self.grandeur)+')'

class Sujet(models.Model):
    concours = models.ForeignKey('concours', on_delete=models.CASCADE)
    annee = models.IntegerField(('year'), validators=[MinValueValidator(1984), max_value_current_year])
    systeme = models.OneToOneField(systeme, on_delete=models.PROTECT, null=True, blank=True)
    SUJET_PT = [('SiA', 'SiA'),('SiB', 'SiB'),('SiC', 'SiC')]
    sujet_pt = models.CharField(max_length=3,choices=SUJET_PT,default='',null=True, blank=True)

    def __str__(self):
        return str(self.systeme)+' ('+str(self.concours)+' '+str(self.annee)+')'

    class Meta:
            ordering = ['systeme__nom']
