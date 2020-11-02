from django.db import models

class ParametresGeneaux(models.Model):
    titre_page=models.CharField(max_length=50, default="GEII")
    nom_etablissement=models.CharField(max_length=100, default="Nom Etablissement")
    auteurs=models.CharField(max_length=100, default="Nom Prénom")
    annee_droits = models.CharField(max_length=100, default="2020")
    github = models.CharField(max_length=150,default="https://github.com/")

class Slide(models.Model):
    img=models.ImageField(null=True, upload_to="slides") #TODO : choose image path
    title=models.CharField(max_length=160)
    description=models.TextField()
