# -*- coding:utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
import unicodedata
from math import ceil

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])


github='https://github.com/Costadoat/'

def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

def annee_scolaire(date):
    if date.month>0 and date.month<9:
        return str(date.year-1)+'-'+str(date.year)
    else:
        return str(date.year)+'-'+str(date.year+1)

class sequence(models.Model):
    numero = models.IntegerField()
    nom = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return "%02d" % self.numero+' '+self.nom

    def str_numero(self):
        return "%02d" % self.numero

    class Meta:
        ordering = ['numero']


class sequence_info(models.Model):
    numero = models.IntegerField()
    nom = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.numero)+' '+self.nom

    def str_numero(self):
        return "%02d" % self.numero

    class Meta:
        ordering = ['numero']


class filiere_prepa(models.Model):
    sigle=models.CharField(max_length=30)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return str(self.sigle)

    class Meta:
            ordering = ['id']


class ecole(models.Model):
    sigle=models.CharField(max_length=30)
    nom = models.CharField(max_length=100)


class concours(models.Model):
    filiere = models.ForeignKey('filiere_prepa', on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom+' ('+str(self.filiere)+')'

    class Meta:
            ordering = ['nom']

class systeme(models.Model):
    nom = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    image = models.FileField(upload_to='systemes/')
    sysml = models.BooleanField(default=False)
    def __str__(self):
        return self.nom

    def uses(self):
        liste_ressources=ressource.objects.filter(systeme=self)
        return len(liste_ressources)

    class Meta:
            ordering = ['nom']

class grandeur(models.Model):
    nom = models.CharField(max_length=100)
    unite = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class parametre(models.Model):
    grandeur = models.ForeignKey('grandeur', on_delete=models.CASCADE)
    valeur = models.FloatField()
    systeme = models.ForeignKey('systeme', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.systeme)+' ('+str(self.grandeur)+')'


class type_de_fichier(models.Model):
    nom = models.CharField(max_length=100)
    icone = models.CharField(max_length=100)
    extension = models.CharField(max_length=100)
    nom_latex = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class type_image_systeme(models.Model):
    nom = models.CharField(max_length=100)
    extension = models.CharField(max_length=100)
    nom_latex = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class fichier_systeme(models.Model):
    type_de_fichier = models.ForeignKey('type_de_fichier', on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    nom_fichier = models.CharField(max_length=100)
    systeme = models.ForeignKey('systeme', on_delete=models.CASCADE)
    def __str__(self):
        return str(self.type_de_fichier)+': '+str(self.nom)
    def url_fichier(self):
        return remove_accents(github + 'Sciences-Ingenieur/raw/master/Systemes/' + self.systeme.nom + '/' + \
                  self.nom_fichier + '.' + self.type_de_fichier.extension)

class image_systeme(models.Model):
    type_image_systeme = models.ForeignKey('type_image_systeme', on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    nom_image = models.CharField(max_length=100)
    systeme = models.ForeignKey('systeme', on_delete=models.CASCADE)
    def __str__(self):
        return str(self.type_image_systeme)+': '+str(self.nom)
    def url_image(self):
        return remove_accents(github + 'Sciences-Ingenieur/raw/master/Systemes/' + self.systeme.nom + '/' + \
                  self.nom_image + '.' + self.type_image_systeme.extension)


class sujet(models.Model):
    concours = models.ForeignKey('concours', on_delete=models.CASCADE)
    annee = models.IntegerField(('year'), validators=[MinValueValidator(1984), max_value_current_year])
    systeme = models.OneToOneField(systeme, on_delete=models.PROTECT, null=True, blank=True)
    SUJET_PT = [('SiA', 'SiA'),('SiB', 'SiB'),('SiC', 'SiC')]
    sujet_pt = models.CharField(max_length=3,choices=SUJET_PT,default='',null=True, blank=True)

    def __str__(self):
        return str(self.systeme)+' ('+str(self.concours)+' '+str(self.annee)+')'

    class Meta:
            ordering = ['systeme__nom']


class famille_competence(models.Model):
    reference = models.CharField(max_length=30)
    nom = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.reference)+' '+self.nom

    def image(self):
        return self.nom.lower().replace('é','e')+'.jp2'

class competence(models.Model):
    famille=models.ForeignKey(famille_competence, on_delete=models.CASCADE)
    parent = models.ManyToManyField('self')
    reference = models.CharField(max_length=30)
    nom = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    semestre = models.IntegerField()
    active = models.BooleanField()

    def __str__(self):
        return str(self.reference)+' '+self.nom

    class Meta:
        ordering = ['id']


class competence_info(models.Model):
    reference = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    active = models.BooleanField()

    def __str__(self):
        return str(self.reference)+' '+self.nom

    class Meta:
        ordering = ['id']


class ressource(models.Model):
    competence = models.ManyToManyField(competence)
    sequence = models.ForeignKey(sequence, on_delete=models.CASCADE)
    numero = models.IntegerField()
    nom = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    systeme = models.ManyToManyField('systeme', blank=True)

    def str_numero(self):
        return "%02d" % self.numero

    def type_de_ressource(self):
        for name in ['cours','td','tp','khole']:
            try:
                attr = getattr(self, name)
                if isinstance(attr, self.__class__):
                    if name=='cours':
                        return name,'C'
                    elif name=='khole':
                        return name,'KH'
                    else:
                        return name,name.upper()
            except:
                pass

    def ilot(self):
        try:
            attr = getattr(self, 'tp')
            return attr.ilot
        except:
            return 0


def url(self,matiere,lien,type,ilot):
    if matiere=='si' and ilot==0:
        dossier = github + 'Sciences-Ingenieur/raw/master/' + str("S%02d" % self.sequence.numero) + ' ' + \
          self.sequence.nom + '/' + type + ("%02d" % self.numero) \
          + " " + self.nom + "/"
        if lien == 'git':
           return dossier
        elif lien == 'pdf':
            return dossier + str("%02d" % self.sequence.numero) + '-' + type + ("%02d" % self.numero) + ".pdf"
        elif lien == 'prive':
            return dossier + str("%02d" % self.sequence.numero) + '-' + type + ("%02d" % self.numero) + "_prive.pdf"
    elif matiere=='si' and ilot!=0:
        dossier = github + 'Sciences-Ingenieur/raw/master/' + str("S%02d" % self.sequence.numero) + ' ' + \
          self.sequence.nom + '/' + type + ("%02d" % self.numero) \
          + " " + self.nom + '/Ilot_' + ("%02d" % ilot) + " " + str(self.nom_ilot()) + '/'
        if lien == 'git':
           return dossier
        elif lien == 'pdf':
            return dossier + str("%02d" % self.sequence.numero) + '-' + type + ("%02d" % self.numero) + '-I' + "%02d" % ilot + ".pdf"
        elif lien == 'prive':
            return dossier + str("%02d" % self.sequence.numero) + '-' + type + ("%02d" % self.numero) + '-I' + "%02d" % ilot + "_prive.pdf"
    else:
        if type == 'C':
            nom_type = 'Cours'
        else:
            nom_type = type
        dossier = github + 'Informatique/raw/master/' + nom_type + '/' + type + ("%02d" % self.numero) \
          + " " + self.nom + "/"
        if lien == 'git':
            return dossier
        elif lien == 'pdf':
            return dossier + 'I-' + type + ("%02d" % self.numero) + ".pdf"
        elif lien == 'prive':
            return dossier + 'I-' + type + ("%02d" % self.numero) + "_prive.pdf"
        elif lien == 'python':
            return dossier + 'Code/I-' + type + ("%02d" % self.numero) + ".py"

class cours(ressource):

    def __str__(self):
        return str("%02d" % self.sequence.numero)+'-'+str("%02d" % self.numero)+' '+self.nom

    def str_numero(self):
        return str("%02d" % self.numero)

    class Meta:
        ordering = ['sequence', 'numero']

    def url_pdf(self):
        return url(self,"si","pdf","C",0)

    def url_prive(self):
        return url(self,"si","prive","C",0)

    def url_git(self):
        return url(self,"si","git","C",0)



class td(ressource):

    def __str__(self):
        return 'S'+str("%02d" % self.sequence.numero)+'-'+str("%02d" % self.numero)+' '+self.nom

    def str_numero(self):
        return str("%02d" % self.numero)

    class Meta:
        ordering = ['sequence', 'numero']

    def url_pdf(self):
        return url(self,"si","pdf","TD",0)

    def url_prive(self):
        return url(self,"si","prive","TD",0)

    def url_git(self):
        return url(self,"si","git","TD",0)


class tp(ressource):
    ilot = models.IntegerField()

    def nom_ilot(self):
        return self.systeme.all()[0]

    def lien_ilot(self):
        return '/systeme/'+str(self.systeme.all()[0].id)

    def __str__(self):
        print(self.id,self.ilot, len(self.systeme.all()))
        if str("%02d" % self.ilot)!='00' and len(self.systeme.all())!=0:
            return 'S'+str("%02d" % self.sequence.numero)+'-'+str("%02d" % self.numero)+' '+self.nom+' Ilot '+str("%02d" % self.ilot)+' ('+self.nom_ilot().nom+')'
        else:
            return 'S'+str("%02d" % self.sequence.numero)+'-'+str("%02d" % self.numero)+' '+self.nom


    def str_numero(self):
        return str("%02d" % self.numero)

    def str_numero_ilot(self):
        return str("%02d" % self.ilot)

    class Meta:
        ordering = ['sequence', 'numero', 'ilot']

    def url_pdf(self):
        return url(self,"si","pdf","TP",self.ilot)

    def url_prive(self):
        return url(self,"si","prive","TP",self.ilot)

    def url_git(self):
        return url(self,"si","git","TP",self.ilot)


class khole(ressource):

    def __str__(self):
        return 'S'+str("%02d" % self.sequence.numero)+'-'+str("%02d" % self.numero)+' '+self.nom

    def str_numero(self):
        return str("%02d" % self.numero)

    class Meta:
        ordering = ['sequence', 'numero']

    def url_pdf(self):
        return url(self,"si","pdf","KH",0)

    def url_prive(self):
        return url(self,"si","prive","KH",0)

    def url_git(self):
        return url(self,"si","git","KH",0)


class ressource_info(models.Model):
    sequence = models.ForeignKey(sequence, on_delete=models.CASCADE)
    numero = models.IntegerField()
    nom = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    def str_numero(self):
        return "%02d" % self.numero


class cours_info(ressource_info):

    def __str__(self):
        return str("%02d" % self.sequence.numero)+'-'+str("%02d" % self.numero)+' '+self.nom

    def str_numero(self):
        return str("%02d" % self.numero)

    class Meta:
        ordering = ['sequence', 'numero']

    def url_pdf(self):
        return url(self,"info","pdf","C",0)

    def url_prive(self):
        return url(self,"info","prive","C",0)

    def url_git(self):
        return url(self,"info","git","C",0)

    def url_python(self):
        return url(self,"info","python","C",0)

class td_info(ressource_info):

    def __str__(self):
        return 'S'+str("%02d" % self.sequence.numero)+'-'+str("%02d" % self.numero)+' '+self.nom

    def str_numero(self):
        return str("%02d" % self.numero)

    class Meta:
        ordering = ['sequence', 'numero']

    def url_pdf(self):
        return url(self,"info","pdf","TD",0)

    def url_prive(self):
        return url(self,"info","prive","TD",0)

    def url_git(self):
        return url(self,"info","git","TD",0)

    def url_python(self):
        return url(self,"info","python","TD",0)


class tp_info(ressource_info):

    def __str__(self):
        return 'S'+str("%02d" % self.sequence.numero)+'-'+str("%02d" % self.numero)+' '+self.nom

    def str_numero(self):
        return str("%02d" % self.numero)

    class Meta:
        ordering = ['sequence', 'numero']

    def url_pdf(self):
        return url(self,"info","pdf","TP",0)

    def url_prive(self):
        return url(self,"info","prive","TP",0)

    def url_git(self):
        return url(self,"info","git","TP",0)

    def url_python(self):
        return url(self,"info","python","TP",0)


class matiere(models.Model):
    nom=models.CharField(max_length=100)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ['id']


class langue_vivante(matiere):
    langue=models.CharField(max_length=100)

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

def url_ds(self, lien):
    dossier = github + 'Sciences-Ingenieur/raw/master/DS/' + annee_scolaire(self.date) +'/DS'+ ("%02d" % self.numero) + "/"
    if lien == 'git':
       return dossier
    elif lien == 'pdf':
        return dossier + 'DS' + str("%02d" % self.numero) + ".pdf"
    elif lien == 'prive':
        return dossier + 'DS' + str("%02d" % self.numero) + "_prive.pdf"

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
    sujet_support=models.ManyToManyField(sujet, blank=True)
    nb_questions=models.IntegerField(null=True, blank=True)
    nb_parties=models.IntegerField(null=True, blank=True)
    coefficients=models.CharField(max_length=100, null=True, blank=True)
    ajustement=models.FloatField(null=True, blank=True)
    question_parties=models.CharField(max_length=100, null=True, blank=True)
    points_parties=models.CharField(max_length=100, null=True, blank=True)
    moyenne=models.FloatField(null=True, blank=True)
    ecart_type=models.FloatField(null=True, blank=True)

    def annee(self):
        return annee_scolaire(self.date)

    def support(self):
        if len(self.sujet_support.all())>0:
            return self.sujet_support.all()[0]
        else:
            return ''

    def __str__(self):
        if len(self.sujet_support.all())>0:
            support=' ('+str(self.sujet_support.all()[0])+')'
        else:
            support=''
        return str(self.date)+' DS'+str(self.numero)+support

    class Meta:
        ordering = ['-date']

    def url_ds_pdf(self):
        return url_ds(self,"pdf")

    def url_ds_prive(self):
        return url_ds(self,"prive")

    def url_ds_git(self):
        return url_ds(self,"git")

    def coefficients_liste(self):
        return [float(x) for x in self.coefficients[1:-1].split(',')]

    def question_parties_liste(self):
        return [int(x) for x in self.question_parties[1:-1].split(',')]

    def points_parties_liste(self):
        return [float(x) for x in self.points_parties[1:-1].split(',')]

    def parties_liste(self):
        parties=[]
        question_parties=self.question_parties_liste()
        points_parties=self.points_parties_liste()
        for i in range(len(question_parties)):
            parties.append([i+1,question_parties[i],points_parties[i]])
        return parties

    def calcul_note(self,coefficients,notes,ajustement,question_parties,points_parties):
        p,l_q=0,0
        note=0
        for (i,n) in enumerate(notes):
            if n=='X':
                n=0
            if i==sum(question_parties[0:p+1]):
                p+=1
                l_q=i
            note+=(points_parties[p]/(5.*sum(coefficients[l_q:question_parties[p]+l_q]))*n*coefficients[i])
        return ceil(note*ajustement*10)/10.

    def notes_eleve_liste(self,etudiant):
        notes_ds=Note.objects.filter(etudiant=etudiant,ds=self).values('value').order_by('id')
        note=[]
        for notes in notes_ds:
            if notes['value']==None or float(notes['value'])==9.0:
                note.append('X')
            else:
                note.append(float(notes['value']))
        return(note)


    def note_eleve(self,etudiant):
        notes_ds=Note.objects.filter(etudiant=etudiant,ds=self).values('value').order_by('id')
        note=[]
        taux=0
        for notes in notes_ds:
            if notes['value']==None or float(notes['value'])==9.0:
                note.append('X')
            else:
                note.append(float(notes['value']))
                taux+=1
        taux='{:2.1f}%'.format(100*taux/len(notes_ds))
        return(self.calcul_note(self.coefficients_liste(),note,self.ajustement,self.question_parties_liste(),self.points_parties_liste()),taux)

    def notes_classe_liste(self):
        etudiants=Note.objects.filter(ds=self).values('etudiant').order_by('etudiant').distinct()
        liste_notes=[]
        for etudiant in etudiants:
            liste_notes.append(self.note_eleve(etudiant['etudiant']))
        return(sorted(liste_notes, reverse = True))

    def classement_eleve(self,etudiant):
        classement=str(self.notes_classe_liste().index(self.note_eleve(etudiant))+1)+'/'+str(len(self.notes_classe_liste()))
        return classement

class Note(models.Model):
    etudiant = models.ForeignKey('Etudiant', on_delete=models.CASCADE)
    numero=models.IntegerField()
    competence = models.ForeignKey('competence', on_delete=models.CASCADE)
    ds = models.ForeignKey('DS', on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ['competence']
