# sendemail/forms.py
from django import forms

class ContactForm(forms.Form):
    expediteur = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class' : 'form-control', 'placeholder': 'Votre adresse mail'}))
    sujet = forms.CharField(required=True, widget=forms.EmailInput(attrs={'class' : 'form-control', 'placeholder': 'Objet de votre demande'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control'}), required=True)
