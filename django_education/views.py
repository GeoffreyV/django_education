# -*-coding: utf-8 -*-

from django import forms
from django.shortcuts import render, redirect, HttpResponseRedirect, render_to_response
from django.contrib.auth import authenticate, logout
from .models import Utilisateur, sequence, cours, famille_competence, competence, cours, td, tp, khole, Note
from quiz.models import Progress

from jchart import Chart
from jchart.config import Axes, DataSet, rgba


def index(request):
    if 'logged_user_id' in request.session:
        logged_user_id=request.session['logged_user_id']
        logged_user=Utilisateur.objects.get(id=logged_user_id)
        return render(request,'index.html', {'logged_user':logged_user})
    else:
        return render(request,'index.html')


def login(request):
    #Teste si le formulaire a été envoyé
    if len(request.POST)>0:
        form = LoginForm(request.POST)
        if form.is_valid():
            user_email=form.cleaned_data['login']
            logged_user=Utilisateur.objects.get(email=user_email)
            request.session['logged_user_id']=logged_user.id
            return redirect('/index')
        else:
            return render(request, 'login.html',{'form': form})
    else:
        form=LoginForm()
        return render(request, 'login.html',{'form': form})

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return redirect('/index')

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

class LineChart(Chart, Progress):
    chart_type = 'line'

    resultats=Progress.objects.all()

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

#def home(request):
#    context = {
#        'radar_chart': RadarChart(),
#    }
#    return render(request, 'test.html', context)

def home(request):
    context = {
        'radar_chart': LineChart(),
    }
    return render(request, 'test.html', context)
