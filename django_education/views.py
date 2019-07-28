# -*-coding: utf-8 -*-

from django import forms
from django.shortcuts import render, redirect, HttpResponseRedirect, render_to_response
from django.contrib.auth import authenticate, logout, login
from .models import Utilisateur, sequence, cours, famille_competence, competence, cours, td, tp, khole, Note, Etudiant
from django.utils import timezone
from django.db.models import Sum, Avg, Func
from django.contrib.auth.decorators import login_required


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
    if 'logged_user_id' in request.session:
        logged_user_id=request.session['logged_user_id']
        logged_user=Utilisateur.objects.get(id=logged_user_id)
        return render(request,'index.html', {'logged_user':logged_user})
    else:
        return render(request,'index.html')

def get_user_by_mail(mail):
    try:
        return Utilisateur.objects.get(email=mail)
    except Utilisateur.DoesNotExist:
        return None

def get_mail_by_username(username):
    try:
        return Utilisateur.objects.get(username=username).email
    except Utilisateur.DoesNotExist:
        return None

class LoginForm(forms.Form):
    login = forms.CharField(label='Mail/Username:')
    password = forms.CharField(label='Mot de passe:', widget = forms.PasswordInput)

    def clean(self):
        cleaned_data=super(LoginForm, self).clean()
        login=cleaned_data.get("login")
        password = cleaned_data.get("password")
        login_by_mail=get_user_by_mail(login)
        if login_by_mail !=None:
            username=login_by_mail
        else:
            username=login
            cleaned_data['login']=get_mail_by_username(login)

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Adresse mail ou mot de passe érroné(e).")

        return cleaned_data


def simple_upload(request):
    if request.method == 'POST':
        new_persons = request.FILES['myfile']
        imported_data = new_persons.read().decode("utf-8")
        lignes = imported_data.split("\n")
        print(imported_data)
    return render(request, 'simple_upload.html')

def lister_ressources(request):
    sequences=sequence.objects.all()
    return render(request, 'sequences.html', {'sequences':sequences})

def afficher_sequence(request, id_sequence):
    sequence_a_afficher=sequence.objects.get(id=id_sequence)
    courss=cours.objects.filter(sequence=id_sequence)
    tds=td.objects.filter(sequence=id_sequence)
    tps=tp.objects.filter(sequence=id_sequence)
    kholes=khole.objects.filter(sequence=id_sequence)
    return render(request, 'sequence.html', {'sequence':sequence_a_afficher,'courss':courss,'tds':tds,'tps':tps,'kholes':kholes})

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



class RadarChart(Chart):
    chart_type = 'radar'

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

def resultats_quizz(request):
    sittings=Sitting.objects.all()
    progresss=Progress.objects.all()
    context = {
        'sittings':sittings, 'progresss':progresss,
    }
    return render(request, 'resultats_quizz.html', context)

def resultats(request, id_etudiant):
    donnees=Sitting.objects.all()
    context = {
        'chart': ResultatsCharts(id_etudiant), 'chart2': RadarChart(), 'general': True, 'donnees':donnees,
    }
    return render(request, 'resultats.html', context)

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


def compte(request):
    context = {
        'radar_chart': LineChart(),
    }
    return render(request, 'compte.html', context)

def mes_quizzes(request):
    context = {
        'radar_chart': LineChart(),
    }
    return render(request, 'mes_quizzes.html', context)

def mes_ds(request):
    context = {
        'radar_chart': LineChart(),
    }
    return render(request, 'resultats_ds.html', context)

def quizzes_etudiants(request):
    context = {
        'radar_chart': LineChart(),
    }
    return render(request, 'quizzes_etudiants.html', context)

def documents(request):
    context = {
        'radar_chart': LineChart(),
    }
    return render(request, 'documents.html', context)

def gestion_ds(request):
    context = {
        'radar_chart': LineChart(),
    }
    return render(request, 'gestion_ds.html', context)

def relative_url_view(request, year, month, day, ext, nom):
    return redirect('/static/upload/'+year+'/'+month+'/'+day+'/'+nom+'.'+ext)
