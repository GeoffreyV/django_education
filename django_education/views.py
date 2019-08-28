# -*-coding: utf-8 -*-

from django.shortcuts import render, redirect, HttpResponseRedirect, render_to_response
from .models import Utilisateur, sequence, sequence_info, famille_competence, competence, cours, cours_info,\
    td, td_info, tp, tp_info, khole, Note, Etudiant, langue_vivante
from quiz.models import Quiz
from django.utils import timezone
from django.db.models import Sum, Avg, Func
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from .forms import ContactForm
import datetime
from jchart import Chart
from jchart.config import Axes, DataSet, rgba


def rentree_scolaire():
    rentree = datetime.datetime.now(tz=timezone.utc)
    unjour = datetime.timedelta(days=1)
    while rentree.month!=8 or rentree.day!=27:
        rentree -= unjour
    return rentree


def index(request):
    return render(request,'index.html')


def upload_eleves(request):
    if request.method == 'POST':
        if 'upload_eleves' in request.POST:
            new_persons = request.FILES['myfile']
            imported_data = new_persons.read().decode("utf-8")
            lignes = imported_data.split("\n")
            for ligne1 in lignes[1:-1]:
                ligne=ligne1.split(',')
                print(ligne)
                user = Utilisateur.objects.create_user(username=ligne[3], email=ligne[3], first_name=ligne[2], last_name=ligne[1], password=ligne[2]+ligne[1], is_student=True)
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
    return render(request, 'sequences.html', {'sequences':sequences, 'si':True})

def lister_ressources_info(request):
    sequences=sequence_info.objects.all()
    return render(request, 'sequences.html', {'sequences':sequences, 'info':True})


def afficher_sequence_si(request, id_sequence):
    sequence_a_afficher=sequence.objects.get(id=id_sequence)
    courss=cours.objects.filter(sequence=id_sequence)
    tds=td.objects.filter(sequence=id_sequence)
    tps=tp.objects.filter(sequence=id_sequence)
    kholes=khole.objects.filter(sequence=id_sequence)
    quizzes=Quiz.objects.filter(category=id_sequence)
    return render(request, 'sequence.html', {'sequence':sequence_a_afficher,'courss':courss,'tds':tds,'tps':tps,'kholes':kholes,'quizzes':quizzes,'si':True})


def afficher_sequence_info(request, id_sequence):
    sequence_a_afficher=sequence_info.objects.get(id=id_sequence)
    courss=cours_info.objects.filter(sequence=id_sequence)
    tds=td_info.objects.filter(sequence=id_sequence)
    tps=tp_info.objects.filter(sequence=id_sequence)
    quizzes=Quiz.objects.filter(category=id_sequence)
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

from quiz.models import Sitting, Progress

@login_required(login_url='/accounts/login/')
def resultats_quizz(request):
    sittings=Sitting.objects.all()
    progresss=Progress.objects.all()
    context = {
        'sittings':sittings, 'progresss':progresss,
    }
    return render(request, 'resultats_quizz.html', context)

@login_required(login_url='/accounts/login/')
def ds_eleve(request, id_etudiant):
    notes_ds=Note.objects.filter(etudiant=id_etudiant).values('id','ds__numero','value','ds').order_by('ds','id')
    liste_ds=[]
    ds=["DS%02d" % (notes_ds[0]['ds__numero'])]
    note=[]
    max_nb_note=0
    for notes in notes_ds:
        if "DS%02d" % (notes['ds__numero'])!=ds[0]:
            if   len(note)>max_nb_note:
                max_nb_note=len(note)
            ds.append(note[:-1])
            ds.append(note[-1])
            note=[]
            liste_ds.append(ds)
            ds=["DS%02d" % (notes['ds__numero'])]
        if float(notes['value'])==9.0:
            note.append('X')
        else:
            note.append(float(notes['value']))
    nb_note=range(max_nb_note)[1:]
    context = {
        'chart': DetailsCharts(id_etudiant), 'liste_ds': liste_ds, 'nb_note': nb_note, 'ds': True,
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

@login_required(login_url='/accounts/login/')
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
        notes_glob_classe = Note.objects.all().exclude(value=9).exclude(competence=0)\
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

@login_required(login_url='/accounts/login/')
class DetailsCharts(Chart):
    chart_type = 'bar'

    def __init__(self, id_etudiant):
        Chart.__init__(self)
        self.etudiants = Etudiant.objects.filter(user__date_joined__gte='2018-09-01').values('user','user__last_name', 'user__first_name')
        self.etudiant_note = Etudiant.objects.filter(user=id_etudiant).values('user','user__last_name', 'user__first_name')
        notes = Note.objects.filter(etudiant=6155).exclude(value=9).exclude(competence=0).values('competence', 'competence__nom', 'competence__reference', 'competence__famille__nom').annotate(moyenne=Round(Avg('value'),2))
        notes_toute_classe = Note.objects.all().exclude(value=9).exclude(competence=0).values('competence', 'competence__nom', 'competence__reference', 'competence__famille__nom').annotate(moyenne=Round(Avg('value'),2))

        self.liste_label=[]
        self.notes_eleve=[]
        self.notes_classe=[]

        for note in notes_toute_classe:
            self.liste_label.append(note['competence__reference'])
            self.notes_classe.append(note['moyenne'])

        index=0

        for note in notes:
            while note['competence__reference']!=self.liste_label[index]:
                self.notes_eleve.append(0)
                index+=1
            self.notes_eleve.append(note['moyenne'])
            index+=1

    def get_etudiant_note(self):
        return self.etudiant_note

    def get_etudiants(self):
        return self.etudiants

    def get_notes_glob(self):
        return zip(self.liste_label,self.notes_eleve,self.notes_classe)

    def get_labels(self):
        return self.liste_label

    def get_datasets(self, **kwargs):
        return [DataSet(label="Elève",
                        color=(64 , 135, 196),
                        data=self.notes_eleve),
                DataSet(label="Classe",
                        color=(179, 181, 198),
                        data=self.notes_classe)]


def relative_url_view(request, year, month, day, ext, nom):
    return redirect('/static/upload/'+year+'/'+month+'/'+day+'/'+nom+'.'+ext)


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
                send_mail(subject, message, sender, recipients)
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
