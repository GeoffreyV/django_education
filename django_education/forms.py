from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(label="Sujet du message ")
    sender = forms.EmailField(label="Expéditeur (à modifier si besoin) ")
    cc_myself = forms.BooleanField(required=False, label="Envoyer une copie sur mon mail ")
    message = forms.CharField(widget=forms.Textarea)
