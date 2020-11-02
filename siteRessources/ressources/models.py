from django.db import models
from django.urls import reverse

class Base(models.Model):
    nom = models.CharField(max_length=100)
    nom_court = nom_court = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=1000, null=True)
    class Meta:
        abstract = True

class Matiere(Base):
    display = models.BooleanField(default=True)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ['id']

    def get_absolute_url(self):
        return reverse('ressources:lister_sequences', args=[str(self.nom_court)])

class Sequence(Base):
    numero = models.IntegerField()
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)

    def __str__(self):
        return "%02d" % self.numero+' - '+self.nom

    def str_numero(self):
        return "%02d" % self.numero

    class Meta:
        ordering = ['numero']

    def get_absolute_url(self):
        return reverse('ressources:lister_sequences', args=[str(self.matiere.nom_court), str(self.numero)])

class Systeme(Base):
    image = models.FileField(upload_to='systemes/')
    sysml = models.BooleanField(default=False)
    matiere = models.ManyToManyField(Matiere, blank=True)

    def __str__(self):
        return self.nom

    def uses(self):
        liste_ressources=ressource.objects.filter(systeme=self)
        return len(liste_ressources)

    class Meta:
            ordering = ['nom']

    def get_absolute_url(self):
        return '/systeme/%i/' % self.id

class Grandeur(models.Model):
    nom = models.CharField(max_length=100)
    unite = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Parametre(models.Model):
    grandeur = models.ForeignKey('grandeur', on_delete=models.CASCADE)
    valeur = models.FloatField()
    systeme = models.ForeignKey('systeme', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.systeme)+' ('+str(self.grandeur)+')'
