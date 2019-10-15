# -*-coding: utf-8 -*-

from django.shortcuts import render, redirect, HttpResponseRedirect, render_to_response
from .models import Utilisateur, sequence, sequence_info, famille_competence, competence, cours, cours_info,\
    td, td_info, tp, tp_info, khole, Note, Etudiant, langue_vivante, DS
from quiz.models import Quiz, Category, Progress
from django.utils import timezone
from django.db.models import Sum, Avg, Func
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import ContactForm
import datetime
from jchart import Chart
from jchart.config import Axes, DataSet, rgba
from math import ceil

github='https://github.com/Costadoat/'

def rentree_scolaire():
    rentree = datetime.datetime.now(tz=timezone.utc)
    unjour = datetime.timedelta(days=1)
    while rentree.month!=8 or rentree.day!=27:
        rentree -= unjour
    return rentree


def index(request):
    return render(request,'index.html')


def upload_eleves(request):

    def remove_space(nom_init):
        nom=nom_init
        while nom[0]==' ':
            nom=nom[1:]
        while nom[-1]==' ':
            nom=nom[:-1]
        return nom

    if request.method == 'POST':
        if 'upload_eleves' in request.POST:
            new_persons = request.FILES['myfile']
            imported_data = new_persons.read().decode("utf-8")
            lignes = imported_data.split("\n")
            for ligne1 in lignes[1:-1]:
                ligne=ligne1.split(';')
                mail=remove_space(ligne[3])
                nom=remove_space(ligne[1])
                prenom=remove_space(ligne[2])
                #La façon dont sont générés les mots de passe est disponible en ligne, il faut donc absolument les modifier.
                user = Utilisateur.objects.create_user(username=mail, email=mail, first_name=prenom, last_name=nom, \
                                                       password=nom.replace('-','').replace("'","").replace(' ','')[0:6].lower() \
                                                                +prenom.replace('-','').replace("'","").replace(' ','')[0:2].lower()\
                                                       , is_student=True)
                etudiant = Etudiant(user=user, annee='PTSI', lv1=langue_vivante.objects.get(langue='Anglais'))
                etudiant.save()
        elif 'upload_ds' in request.POST:
            new_persons = request.FILES['myfile']
            imported_data = new_persons.read().decode("iso8859-1")
            lignes = imported_data.split("\n")
            print(imported_data[0])
        return render(request, 'simple_upload.html',{'done': True})
    return render(request, 'simple_upload.html')


def lister_ressources_si(request):
    sequences=sequence.objects.all()
    dossier_ds = github + 'Sciences-Ingenieur/raw/master/DS/'
    return render(request, 'sequences.html', {'sequences':sequences, 'dossier_ds':dossier_ds, 'si':True})

def lister_ressources_info(request):
    sequences=sequence_info.objects.all()
    dossier_ds = github + 'Informatique/raw/master/DS/'
    return render(request, 'sequences.html', {'sequences':sequences, 'dossier_ds':dossier_ds, 'info':True})


def afficher_sequence_si(request, id_sequence):
    sequence_a_afficher=sequence.objects.get(id=id_sequence)
    courss=cours.objects.filter(sequence=id_sequence)
    tds=td.objects.filter(sequence=id_sequence)
    tps=tp.objects.filter(sequence=id_sequence)
    kholes=khole.objects.filter(sequence=id_sequence)
    quizzes=Quiz.objects.filter(category__category__startswith="SI-S%02d" % id_sequence)
    return render(request, 'sequence.html', {'sequence':sequence_a_afficher,'courss':courss,'tds':tds,'tps':tps,'kholes':kholes,'quizzes':quizzes,'si':True})


def afficher_sequence_info(request, id_sequence):
    sequence_a_afficher=sequence_info.objects.get(id=id_sequence)
    courss=cours_info.objects.filter(sequence=id_sequence)
    tds=td_info.objects.filter(sequence=id_sequence)
    tps=tp_info.objects.filter(sequence=id_sequence)
    quizzes=Quiz.objects.filter(category__category="Info-S%02d" % id_sequence)
    return render(request, 'sequence.html', {'sequence':sequence_a_afficher,'courss':courss,'tds':tds,'tps':tps,'quizzes':quizzes,'info':True})


def lister_competences(request):
    competences=famille_competence.objects.all()
    return render(request, 'competences.html', {'competences':competences})


def afficher_famille_competence(request, id_famille):
    famille=famille_competence.objects.get(id=id_famille)
    competence_a_afficher=competence.objects.filter(famille=id_famille)
    return render(request, 'competence.html', {'famille':famille,'competences':competence_a_afficher})

def afficher_competence(request, id_famille, id_competence):
    famille=famille_competence.objects.get(id=id_famille)
    competence_a_afficher=competence.objects.get(id=id_competence)
    courss=cours.objects.filter(competence=id_competence)
    tds=td.objects.filter(competence=id_competence)
    tps=tp.objects.filter(competence=id_competence)
    kholes=khole.objects.filter(competence=id_competence)
    return render(request, 'competence_seule.html', {'famille':famille,'competence':competence_a_afficher, 'courss':courss, 'tds':tds, 'tps':tps,'kholes':kholes})


class LineChart(Chart):
    chart_type = 'line'


    def get_labels(self):
        return ["Eating", "Drinking", "Sleeping", "Designing", "Coding", "Cycling", "Running"]

    def get_datasets(self, **kwargs):
        return [DataSet(label="My First dataset",
                        color=(179, 181, 198),
                        data=[65, 59, 90, 81, 56, 55, 40]),
                DataSet(label="My Second dataset",
                        color=(255, 99, 132),
                        data=[28, 48, 40, 19, 96, 27, 100])]


def chart(request):
    context = {
        'radar_chart': LineChart(),
    }
    return render(request, 'chart.html', context)

@login_required(login_url='/accounts/login/')
def resultats_vierge(request):
    etudiants = Etudiant.objects.filter(user__date_joined__gte=rentree_scolaire()).values('user')[0]['user']
    return redirect('/resultats/'+str(etudiants)+'/')

@login_required(login_url='/accounts/login/')
def resultats_quizz(request):
    #sittings=Sitting.objects.all().order_by('user')
    eleves=Etudiant.objects.filter(annee='PTSI').select_related('progress')\
        .values('user__last_name','user__first_name', 'user__progress__score').order_by('user__last_name','user__first_name')
    categories=Category.objects.all()
    cats=[]
    for categorie in categories:
        cats.append(categorie.category)
    notes_triees=[]
    for eleve in eleves:
        notes=str(eleve['user__progress__score']).split(',')
        notes_triees_eleve=[['#FFFFFF','-/-'] for i in range(len(cats))]
        for cat in cats:
            try:
                test_col=float(notes[notes.index(cat)+1])/float(notes[notes.index(cat)+2])
                if test_col<0.3:
                    color='#f01547'
                elif test_col >=0.3 and test_col<0.7:
                    color='#ff5733'
                elif test_col>=0.7:
                    color='#3dd614'
                notes_triees_eleve[notes.index(cat)//3]=[color,str(notes[notes.index(cat)+1])+'/'+str(notes[notes.index(cat)+2])]
            except ValueError:
                thing_index = -1
        notes_triees.append([eleve['user__last_name'].replace(' "','').replace('" ','').replace('"',''), \
                             eleve['user__first_name'].replace(' "','').replace('" ','').replace('"',''),notes_triees_eleve])
    context = {
    'notes_triees':notes_triees, 'cats':cats
    }
    return render(request, 'resultats_quizz.html', context)

def calcul_note(coefficients,notes,ajustement,question_parties,points_parties):
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

@login_required(login_url='/accounts/login/')
def ds_eleve(request, id_etudiant):
    notes_ds=Note.objects.filter(etudiant=id_etudiant).values('id','ds__type_de_ds','ds__numero','value','ds').order_by('ds','id')
    ds=DS.objects.get(id=notes_ds[0]['ds'])
    coefficients=[int(x) for x in ds.coefficients[1:-1].split(',')]
    question_parties=[int(x) for x in ds.question_parties[1:-1].split(',')]
    points_parties=[int(x) for x in ds.points_parties[1:-1].split(',')]
    parties=[]
    for i in range(len(question_parties)):
        parties.append([i+1,question_parties[i],points_parties[i]])
    note=[]
    liste_ds=[]
    for notes in notes_ds:
        if notes['ds']==ds.id:
            if notes['value']==None:
                note.append('X')
            elif float(notes['value'])==9.0:
                note.append('X')
            else:
                note.append(float(notes['value']))
        else:
            note=[]
            ds=DS.objects.get(id=notes_ds[0]['ds'])
            coefficients=[int(x) for x in ds.coefficients[1:-1].split(',')]
            question_parties=[int(x) for x in ds.question_parties[1:-1].split(',')]
            points_parties=[int(x) for x in ds.points_parties[1:-1].split(',')]
            parties=[]
            for i in range(len(question_parties)):
                parties.append([i,question_parties[i],points_parties[i]])
            liste_ds.append([ds,note,range(1,len(note)+1),coefficients,parties,calcul_note(coefficients,note,ds.ajustement,question_parties,points_parties)])
    liste_ds.append([ds,note,range(1,len(note)+1),coefficients,parties,calcul_note(coefficients,note,ds.ajustement,question_parties,points_parties)])
    context = {
        'chart': DetailsCharts(id_etudiant), 'liste_ds': liste_ds, 'coefficients' : coefficients, 'ds': True,
    }

    return render(request, 'resultats.html', context)

@login_required(login_url='/accounts/login/')
def resultats(request, id_etudiant):
    if request.user.is_teacher or (request.user.is_student and request.user.id==id_etudiant):
        context = {
            'chart': ResultatsCharts(id_etudiant), 'general': True,
        }
        return render(request, 'resultats.html', context)
    else:
        return render(request, '/index')

@login_required(login_url='/accounts/login/')
def details(request, id_etudiant):
    context = {
        'chart': DetailsCharts(id_etudiant), 'details': True,
    }
    return render(request, 'resultats.html', context)

class Round(Func):
    function = 'ROUND'
    arity = 2


class ResultatsCharts(Chart):

    chart_type = 'radar'
    options = {
        'scale': {'ticks': {
                'suggestedMin': 0,
                'suggestedMax': 5,
                'stepSize': 1,

            }}
    }
    def __init__(self, id_etudiant):
        Chart.__init__(self)
        self.etudiants = Etudiant.objects.filter(user__date_joined__gte=rentree_scolaire()).values('user','user__last_name', 'user__first_name')
        self.etudiant_note = Etudiant.objects.filter(user=id_etudiant).values('user','user__last_name', 'user__first_name')
        notes_glob = Note.objects.filter(etudiant=id_etudiant).exclude(value=9).exclude(competence=0)\
            .values('competence__famille__nom').annotate(moyenne=Round(Avg('value'),2))\
            .order_by('competence__famille__nom')
        notes_glob_classe = Note.objects.filter(etudiant__user__date_joined__gte=rentree_scolaire()).exclude(value=9).exclude(competence=0)\
            .values('competence__famille__nom').annotate(moyenne=Round(Avg('value'),2))\
            .order_by('competence__famille__nom')

        self.liste_label=[]
        self.notes_eleve=[]
        self.notes_classe=[]

        for note in notes_glob_classe:
            self.liste_label.append(note['competence__famille__nom'])
            self.notes_classe.append(note['moyenne'])

        index=0

        for note in notes_glob:
            while note['competence__famille__nom']!=self.liste_label[index]:
                self.notes_eleve.append(0)
                index+=1
            self.notes_eleve.append(note['moyenne'])
            index+=1

    def get_options(self):
        options = {
            "scale": {
                "display": False,
                "ticks": {
                    "minDataValue": 0,
                    "maxDataValue": 5
                }
            }
        }
        return options

    def get_notes_glob(self):
        return zip(self.liste_label,self.notes_eleve,self.notes_classe)

    def get_labels(self):
        return self.liste_label

    def get_etudiant_note(self):
        return self.etudiant_note

    def get_etudiants(self):
        return self.etudiants

    def get_datasets(self, **kwargs):
        return [DataSet(label="Elève",
                        color=(64 , 135, 196),
                        data=self.notes_eleve),
                DataSet(label="Classe",
                        color=(179, 181, 198),
                        data=self.notes_classe)]

class DetailsCharts(Chart):
    chart_type = 'bar'
    options= {
            "scales": {
                "yAxes": [{
                    "ticks": {
                        "suggestedMin": 0,
                        "suggestedMax": 5
                    }
                }]
            }
    }

    def __init__(self, id_etudiant):
        Chart.__init__(self)
        self.etudiants = Etudiant.objects.filter(user__date_joined__gte=rentree_scolaire()).values('user','user__last_name', 'user__first_name')
        self.etudiant_note = Etudiant.objects.filter(user=id_etudiant).values('user','user__last_name', 'user__first_name')
        notes = Note.objects.filter(etudiant__user=id_etudiant).exclude(value=9).exclude(competence=0)\
            .values('competence', 'competence__famille', 'competence__nom', 'competence__reference', 'competence__famille__nom')\
            .annotate(moyenne=Round(Avg('value'),2)).order_by('competence__reference')
        notes_toute_classe = Note.objects.filter(etudiant__user__date_joined__gte=rentree_scolaire())\
            .exclude(value=9).exclude(competence=0).values('competence', 'competence__famille', 'competence__nom', 'competence__reference', 'competence__famille__nom')\
            .annotate(moyenne=Round(Avg('value'),2)).order_by('competence__reference')
        self.liste_label=[]
        self.liste_comp=[]
        self.notes_eleve=[]
        self.notes_classe=[]

        for note in notes_toute_classe:
            self.liste_comp.append([note['competence'],note['competence__famille'],note['competence__reference'],note['competence__nom'],"","danger"])
            self.liste_label.append(note['competence__reference'])
            self.notes_classe.append(note['moyenne'])

        index=0

        for note in notes:
            while note['competence']!=self.liste_comp[index][0]:
                self.liste_comp[index][4]=0
                self.notes_eleve.append(0)
                index+=1
            if note['moyenne']>3.5:
                self.liste_comp[index][5]="success"
            elif note['moyenne']>1.5:
                self.liste_comp[index][5]="warning"
            self.notes_eleve.append(note['moyenne'])
            self.liste_comp[index][4]=note['moyenne']
            index+=1

    def get_liste_comp(self):
        return self.liste_comp

    def get_etudiant_note(self):
        return self.etudiant_note

    def get_etudiants(self):
        return self.etudiants

    def get_notes_glob(self):
        return zip(self.liste_label,self.notes_eleve,self.notes_classe)

    def get_labels(self):
        return self.liste_label

    def get_datasets(self, **kwargs):
        print(self.notes_eleve)
        return [DataSet(label="Elève",
                        color=(64 , 135, 196),
                        data=self.notes_eleve),
                DataSet(label="Classe",
                        color=(179, 181, 198),
                        data=self.notes_classe)]


def relative_url_view(request, nomquiz, action, year, month, day, ext, nom):
    return redirect('/static/uploads/'+year+'/'+month+'/'+day+'/'+nom+'.'+ext)


def contact(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']

            recipients = ['costadoat@crans.org']
            if cc_myself:
                recipients.append(sender)
            if subject and message and sender:
                send_mail('[Costadoat.fr] '+subject, message, sender, recipients)
                return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        if request.user.is_authenticated:
            form = ContactForm(initial={'sender': request.user.email})
        else:
            form = ContactForm()
    return render(request, 'contact.html', {'form': form, 'thanks': False})


def thanks(request):
    return render(request, 'contact.html', {'thanks': True})
