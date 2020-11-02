from django.db import models
from django.urls import reverse

from .general import ParametresGeneaux

class Base(models.Model):
    nom = models.CharField(max_length=100)
    nom_court = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)

    def str_numero(self):
        return ""

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
        return reverse('ressources:lister_ressources', args=[str(self.matiere.nom_court), str(self.numero)])

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

class Famille_competence(models.Model):
    reference = models.CharField(max_length=30)
    nom = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.reference)+' '+self.nom

    def image(self):
        return self.nom.lower().replace('é','e')+'.jp2'

class Competence(models.Model):
    famille=models.ForeignKey(Famille_competence, on_delete=models.CASCADE)
    parent = models.ManyToManyField('self', blank=True)
    reference = models.CharField(max_length=30)
    nom = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    semestre = models.IntegerField()
    active = models.BooleanField()
    matiere = models.ManyToManyField(Matiere)

    def __str__(self):
        return str(self.reference)+' '+self.nom

    class Meta:
        ordering = ['id']

    def get_absolute_url(self):
        return '/competence/%i/%i' % (self.famille.id,self.id)


RESSOURCE_TYPE = (
    ('C', 'Cours'),
    ('KH', 'Khole'),
    ('TD', 'Travaux Dirigés'),
    ('TP', 'Travaux Pratiques'),
    ('V', 'Video')
)

class Ressource(models.Model):
    type = models.CharField(max_length=2, choices=RESSOURCE_TYPE)
    competence = models.ManyToManyField(Competence)
    sequence = models.ForeignKey(Sequence, on_delete=models.CASCADE)
    numero = models.IntegerField()
    nom = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    systeme = models.ManyToManyField('Systeme', blank=True)

    def __str__(self):
        return 'S'+str("%02d" % self.sequence.numero)+'-' + self.type +str("%02d" % self.numero)+' '+self.nom

    def reference(self):
        return 'S'+str("%02d" % self.sequence.numero)+'-' + self.type + str("%02d" % self.numero)

    def str_numero(self):
        return str("%02d" % self.numero)

    def get_github_folder(self):
        folder =  ParametresGeneaux.objects.first().github + self.sequence.nom_court + '/raw/master/' + str("S%02d" % self.sequence.numero) + ' ' + \
          self.sequence.nom + '/' + self.type + ("%02d" % self.numero) \
          + " " + self.nom + "/"
        return folder

    def url_pdf(self):
        url = self.get_github_folder() + self.reference() + '.pdf'
        return url

    def url_prive(self):
        url = self.get_github_folder() + self.reference() + '_prive.pdf'
        return url

    def url_git(self):
        return self.get_github_folder()

    class Meta:
        ordering = ['sequence', 'numero']

    def exist_video(self):
        return video.objects.filter(ressource=self)

    def exist_fiche(self):
        return fiche_synthese.objects.get(ressource=self)

# Cours
class CoursManager(models.Manager):
    def get_queryset(self):
        return super(CoursManager, self).get_queryset().filter(
            type='C')

class Cours(Ressource):

    objects = CoursManager()

    class Meta:
        ordering = ['sequence', 'numero']
        proxy = True

# TD
class TDManager(models.Manager):
    def get_queryset(self):
        return super(TDManager, self).get_queryset().filter(
            type='TD')
class Td(Ressource):

    objects = TDManager()

    class Meta:
        ordering = ['sequence', 'numero']
        proxy = True

# TP

class TPManager(models.Manager):
    def get_queryset(self):
        return super(TPManager, self).get_queryset().filter(
            type='TP')

class Tp(Ressource):

    objects = TPManager()

    def ilots(self):
        ilots=Ilot.objects.filter(tp=self)
        return ilots

    class Meta:
        ordering = ['sequence', 'numero']
        proxy = True

class Ilot(models.Model):
    parent = models.ForeignKey(Ressource, on_delete=models.CASCADE)
    numero = models.IntegerField()
    systeme = models.ForeignKey(Systeme, on_delete=models.CASCADE, null=True)

    def __str__(self):
            return 'S'+str("%02d" % self.parent.sequence.numero)+'-TP'\
            +str("%02d" % self.parent.numero)+'-I'+str("%02d" % self.numero)\
            +' ('+str(self.systeme.nom)+')'

    def nom_court(self):
        return str("%02d" % self.numero)+' '+self.systeme.nom

    def nom(self):
        return str("%02d" % self.numero)+' '+self.systeme.nom

    class Meta:
        ordering = ['parent', 'numero']

    def get_github_folder(self):
        return self.parent.get_github_folder() + 'Ilot_' + str(self.numero) + " " + self.systeme.nom + "/"


    def url_pdf(self):
        url =  self.get_github_folder() + self.parent.reference()+ ".pdf"
        return url

    def url_prive(self):
        url =  self.get_github_folder() + self.parent.reference() + "_prive.pdf"
        return url

    def url_git(self):
        url =  self.get_github_folder()
        return url

# Kholes

class KholeManager(models.Manager):
    def get_queryset(self):
        return super(KholeManager, self).get_queryset().filter(
            type='KH')

class Khole(Ressource):

    objects = KholeManager()

    class Meta:
        proxy=True

class Video(Ressource):
    ressource = models.ForeignKey(Ressource, on_delete=models.CASCADE, null=True, related_name='ressource_associee')
    nom_fichier = models.CharField(max_length=100)


    def url(self):
        dossier = github + 'Sciences-Ingenieur/raw/master/' + str("S%02d" % self.ressource.sequence.numero) + ' ' + \
              self.ressource.sequence.nom +'/'+self.ressource.type_de_ressource()[1]+str("%02d" % self.ressource.numero)+' '+self.ressource.nom+ \
             '/Videos/'
        return dossier+self.nom_fichier+'?raw=true'
