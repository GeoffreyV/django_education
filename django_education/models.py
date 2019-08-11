# -*- coding:utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser

github='https://github.com/Costadoat/S'

class sequence(models.Model):
    numero = models.IntegerField()
    nom = models.CharField(max_length=35)
    description = models.CharField(max_length=500)
    def __str__(self):
        return "%02d" % self.numero+' '+self.nom
    def str_numero(self):
        return "%02d" % self.numero
    class Meta:
        ordering = ['numero']

class sequence_info(models.Model):
    numero = models.IntegerField()
    nom = models.CharField(max_length=35)
    description = models.CharField(max_length=500)
    def __str__(self):
        return str(self.numero)+' '+self.nom

class filiere_prepa(models.Model):
    sigle=models.CharField(max_length=35)
    nom = models.CharField(max_length=50)
    def __str__(self):
        return self.sigle
    class Meta:
            ordering = ['id']

class ecole(models.Model):
    sigle=models.CharField(max_length=35)
    nom = models.CharField(max_length=50)

class concours(models.Model):
    filiere = models.ForeignKey('filiere_prepa', on_delete=models.CASCADE)


class sujet(models.Model):
    concours = models.ForeignKey('concours', on_delete=models.CASCADE)
    annee = models.DateField()

class systeme(models.Model):
    nom = models.CharField(max_length=35)
    description = models.CharField(max_length=500)
    img = models.CharField(max_length=30)
    sujet = models.OneToOneField(sujet, on_delete=models.PROTECT, null=True, blank=True)
    def __str__(self):
        return self.nom
    class Meta:
            ordering = ['id']

class famille_competence(models.Model):
    reference = models.CharField(max_length=10)
    nom = models.CharField(max_length=35)
    description = models.CharField(max_length=500)
    def __str__(self):
        return str(self.reference)+' '+self.nom
    def image(self):
        return self.nom.lower().replace('é','e')+'.jpg'

class competence(models.Model):
    famille=models.ForeignKey(famille_competence, on_delete=models.CASCADE)
    parent = models.ManyToManyField('self')
    reference = models.CharField(max_length=10)
    nom = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    semestre = models.IntegerField()
    active = models.BooleanField()
    def __str__(self):
        return str(self.reference)+' '+self.nom
    class Meta:
            ordering = ['id']

class ressource(models.Model):
    competence = models.ManyToManyField(competence)
    sequence = models.IntegerField()
    numero = models.IntegerField()
    nom = models.CharField(max_length=35)
    description = models.CharField(max_length=500)
    systeme = models.ManyToManyField('systeme')
    def str_numero(self):
        return "%02d" % self.numero


def url(self,lien,type):
    dossier=github+("%02d" % self.sequence)+"/raw/master/"+type+("%02d" % self.numero)\
                 +" "+self.nom+"/"
    if lien=='git':
        return dossier
    elif lien=='pdf':
        return dossier+("%02d" % self.sequence)+"-"+type+("%02d" % self.numero)+".pdf"
    elif lien=='prive':
        return dossier+("%02d" % self.sequence)+"-"+type+("%02d" % self.numero)+"_prive.pdf"

class cours(ressource):
    def __str__(self):
        return 'S'+str("%02d" % self.sequence)+'-'+str("%02d" % self.numero)+' '+self.nom
    def str_numero(self):
        return str("%02d" % self.numero)
    class Meta:
                ordering = ['sequence', 'numero']
    def url_pdf(self):
        return url(self,"pdf","C")
    def url_prive(self):
        return url(self,"prive","C")
    def url_git(self):
        return url(self,"git","C")


class td(ressource):
    def __str__(self):
        return 'S'+str("%02d" % self.sequence)+'-'+str("%02d" % self.numero)+' '+self.nom
    def str_numero(self):
        return str("%02d" % self.numero)
    pass
    class Meta:
                ordering = ['sequence', 'numero']
    def url_pdf(self):
        return url(self,"pdf","TD")
    def url_prive(self):
        return url(self,"prive","TD")
    def url_git(self):
        return url(self,"git","TD")

class tp(ressource):
    ilot = models.IntegerField()
    def nom_ilot(self):
        return self.systeme.all()[0]
    def __str__(self):
        return 'S'+str("%02d" % self.sequence)+'-'+str("%02d" % self.numero)+' '+self.nom
    def str_numero(self):
        return str("%02d" % self.numero)
    def str_numero_ilot(self):
        return str("%02d" % self.ilot)
    class Meta:
                ordering = ['sequence', 'numero']
    def url_pdf(self):
        return url(self,"pdf","TP")
    def url_prive(self):
        return url(self,"prive","TP")
    def url_git(self):
        return url(self,"git","TP")

class khole(ressource):
    def __str__(self):
        return 'S'+str("%02d" % self.sequence)+'-'+str("%02d" % self.numero)+' '+self.nom
    def str_numero(self):
        return str("%02d" % self.numero)
    class Meta:
                ordering = ['sequence', 'numero']
    def url_pdf(self):
        return url(self,"pdf","KH")
    def url_prive(self):
        return url(self,"prive","KH")
    def url_git(self):
        return url(self,"git","KH")

class ressource_info(models.Model):
    sequence = models.IntegerField()
    numero = models.IntegerField()
    nom = models.CharField(max_length=35)
    description = models.CharField(max_length=500)

class cours_info(ressource_info):
    prerequis=models.ManyToManyField('self')

class td_info(ressource_info):
    pass

class tp_info(ressource_info):
    pass

class matiere(models.Model):
    def __str__(self):
        return self.nom
    nom=models.CharField(max_length=30)
    class Meta:
        ordering = ['id']


class langue_vivante(matiere):
    langue=models.CharField(max_length=35)
    def __str__(self):
        return self.langue
    class Meta:
        ordering = ['id']

class Utilisateur(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)
    def __str__(self):
        return self.last_name+' '+self.first_name+' ('+self.username+')'

class Etudiant(models.Model):
    user = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, primary_key=True)
    ANNEE = [
        ('PTSI', 'PTSI'),
        ('PT', 'PT')
    ]
    annee = models.CharField(
        max_length=4,
        choices=ANNEE,
        default='PTSI',
    )
    lv1 = models.ForeignKey('langue_vivante', on_delete=models.PROTECT)
#    quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')
    def __str__(self):
        return self.user.last_name+' '+self.user.first_name

class Professeur(models.Model):
    user = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, primary_key=True)

    ANNEE = [
        ('PTSI', 'PTSI'),
        ('PTSI/PT', 'PTSI/PT'),
        ('PT', 'PT')
    ]
    annee = models.CharField(
        max_length=7,
        choices=ANNEE,
        default='PTSI',
    )
    matiere = models.ForeignKey('matiere', on_delete=models.PROTECT)
    def __str__(self):
        return self.user.last_name+' '+self.user.first_name

class DS(models.Model):
    TYPE_DE_DS = [
        ('DS', 'DS'),
        ('DM', 'DM'),
        ('Cours', 'Cours'),
        ('CB', 'CB')
    ]
    type_de_ds=models.CharField(
        max_length=5,
        choices=TYPE_DE_DS,
        default='DS',
    )
    numero = models.IntegerField()
    date = models.DateField()
    nom=models.CharField(max_length=30)

class Note(models.Model):
    etudiant = models.ForeignKey('Etudiant', on_delete=models.CASCADE)
    competence = models.ForeignKey('competence', on_delete=models.CASCADE)
    ds = models.ForeignKey('DS', on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=4, decimal_places=2)
    class Meta:
        ordering = ['competence']
