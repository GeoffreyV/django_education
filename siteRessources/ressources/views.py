from django.shortcuts import render
from .models import Slide, Matiere, Famille_competence, Sequence, Cours, Video, Td, Tp, Khole, Ilot

def index(request):
    slides = Slide.objects.all()
    return render(request,'ressources/index.html',{'slides':slides})

def lister_sequences(request,matiere):
    if (Matiere.objects.filter(nom_court=matiere).exists()):
        matiere = Matiere.objects.get(nom_court=matiere)
        sequences = matiere.sequence_set.all()
        return render(request, 'ressources/lister_items.html', {'items_list':sequences, 'titre': matiere.nom + ' - ' + "Séquences"})
    else:
        return render(request, '404.html')

def lister_systemes(request, matiere):
    if (Matiere.objects.filter(nom_court=matiere).exists()):
        matiere = Matiere.objects.get(nom_court=matiere)
        systemes = matiere.systeme_set.all()
        return render(request, 'ressources/lister_items.html', {'items_list':systemes, 'titre': matiere.nom + ' - ' + "Systèmes"})
    else:
        return render(request, '404.html')

def lister_ressources(request, matiere, sequence_id):
    if(Sequence.objects.filter(matiere__nom_court=matiere).filter(numero=sequence_id).exists):
        sequence_a_afficher=Sequence.objects.filter(matiere__nom_court=matiere).get(numero=sequence_id)
        ressources = {}
        if ( Cours.objects.filter(sequence__numero=sequence_id) ):
            ressources['Cours'] = Cours.objects.filter(sequence__numero=sequence_id)
        if ( Video.objects.filter(ressource__sequence__numero=sequence_id) ):
            ressources['Vidéo'] = Video.objects.filter(ressource__sequence__numero=sequence_id)
        if ( Td.objects.filter(sequence__numero=sequence_id) ):
            ressources['TD']    = Td.objects.filter(sequence__numero=sequence_id)
        if ( Tp.objects.filter(sequence__numero=sequence_id)):
            ressources['TP']    = Tp.objects.filter(sequence__numero=sequence_id)
            liste_ilots=[]
            for tp_one in ressources['TP']:
                ilots=Ilot.objects.filter(parent=tp_one)
                liste_ilots.append([tp_one,ilots])
        if ( Khole.objects.filter(sequence__numero=sequence_id) ):
            ressources['kholles'] = Khole.objects.filter(sequence__numero=sequence_id)
        # if ( Quiz.objects.filter(category__category__startswith="SI-S%02d" % sequence_id) ):
        #     ressources['Kholles'] = Quiz.objects.filter(category__category__startswith="SI-S%02d" % sequence_id)
        return render(request, 'ressources/lister_ressources.html', {'sequence':sequence_a_afficher,'matiere':Matiere.objects.get(nom_court=matiere),'ressources':ressources})
    else:
        return render(request, '404.html')

def lister_ds(request, matiere):
    if (Matiere.objects.filter(nom_court=matiere).exists()):
        matiere = Matiere.objects.get(nom_court=matiere)
        ds = matiere.ds_set.all()
        return render(request, 'ressources/lister_items.html', {'items_list':systemes, 'titre': matiere+ ' - ' + "DS"})
    else:
        return render(request, '404.html')

def lister_competences(request, matiere):
    competences=Famille_competence.objects.all()
    return render(request, 'ressources/lister_items.html', {'competences':competences})
