from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.apps import apps
from .models import Delitsplus, Personnegrc, Municipalite, Liberation, Province
from django.contrib import messages
from .forms import PersonneForm, DelitsplusForm, LiberationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, StreamingHttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
#A necessite l'installation de reportlab (pip install reportlab)
import datetime
import csv
#from django.db import connection


@login_required(login_url=settings.LOGIN_URI)
def choixntp1province(request):
    entete = "Reprise NTP1 GRC : Choix de la province"
    provinces = Province.objects.all()
    if request.method == 'POST':
        return redirect(listentp1personne, request.POST.get('provinceid') )
    else:
        return render(request, 'choixprovincentp1.html', {'provinces': provinces, 'entete': entete})


## Affiche la liste des dossiers encore ouverts
@login_required(login_url=settings.LOGIN_URI)
def listentp1personne(request, pi):
    entete = "Reprise NTP1 GRC : Listing"
    personne_list = Personnegrc.objects.filter(Q(ferme=0) & Q(province=pi))
    paginator = Paginator(personne_list, 100)
    page = request.GET.get('page')
    try:
        personnes = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        personnes = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        personnes = paginator.page(paginator.num_pages)
    return render(request, 'listentp1grc.html', {'personnes': personnes, 'entete': entete})


## Pour vérifier si de nouveaux délits sont présents dans les fiches
@login_required(login_url=settings.LOGIN_URI)
def personnentp1edit(request, pk):
    personne = Personnegrc.objects.get(pk=pk)
    entete = "Reprise NTP1 GRC : Mise à jour"
    date_old_sentence = datetime.date(1900, 1, 1)
    oldfps = personne.oldpresencefps
    if Delitsplus.objects.filter(personnegrc=personne).exists():
        dernieredate = Delitsplus.objects.filter(personnegrc=personne).order_by('-date_sentence').first()
        date_old_sentence = dernieredate.date_sentence

    if request.method == 'POST':
        form = PersonneForm(request.POST, instance=personne)
        if form.is_valid():
            personne = form.save(commit=False)
            personne.RA = request.user
            # print(request.POST.get('dateprint2').__class__)
            newfps = request.POST.get('newpresencefps')
            date_new_sentence = datetime.date(1900, 1, 1)
            if request.POST.get('dateverdictder') != "":
                an, mois, jour = request.POST.get('dateverdictder').split('-')
                date_new_sentence = datetime.date(int(an), int(mois), int(jour))
            timediff = date_new_sentence - date_old_sentence
            if timediff.days > 1:
                personne.newdelit = 1
                messages.success(request, "La personne a été mise à jour.")
            else:
                personne.newdelit = 0
                personne.ferme = 1
                messages.success(request, "La personne a été mise à jour et le dossier fermé.")
            personne.save()
            if (date_new_sentence > date_old_sentence) | (oldfps == 0 and newfps == 1):
                return redirect('personnentp1delits', personne.id)
            else:
                return redirect('listentp1personne', personne.province_id)
        else:
            messages.error(request, "Il y a une erreur dans l'enregistrement")
            return redirect('personnentp1edit', personne.id)
    else:
        form = PersonneForm(instance=personne)
    return render(request, "personnentp1edit.html", {'my_form': form, 'entete': entete, 'personne': personne})


## Permet sur une même page d'enregistrer les délits, les libérations et de voir ce qui est déjà rentré
@login_required(login_url=settings.LOGIN_URI)
def personnentp1delits(request, pk):
    personne = Personnegrc.objects.get(pk=pk)
    delits = Delitsplus.objects.filter(personnegrc=personne).order_by('-date_sentence')
    liberations = Liberation.objects.filter(personnegrc=personne).order_by('-date_liberation')
    entete = "Reprise NTP1 GRC : Délits "
    # Fait la liste des villes de la province correspondante et ajoute les autres
    ville = Municipalite.objects.filter(Q(province=personne.province) | Q(province=5))
    form = DelitsplusForm(prefix='delit')
    form.fields['lieu_sentence'].queryset = ville
    libe_form = LiberationForm(prefix='libe')
    if request.method == 'POST':
        if 'Savelibe' or 'Savelibequit' in request.POST:
            libe_form = LiberationForm(request.POST, prefix='libe')
            form = DelitsplusForm(prefix='delit')
            if libe_form.is_valid():
                libe = libe_form.save(commit=False)
                libe.RA = request.user
                libe.personnegrc = personne
                libe.save()
                messages.success(request, "Une liberation de " + str(personne.codeGRC) + " a été ajoutée.")
                if 'Savelibequit' in request.POST:
                    return redirect('listentp1personne', personne.province_id)
                elif 'Savelibe':
                    return redirect('personnentp1delits', personne.id )
        if not libe_form.is_valid():
            if 'Savequit' or 'Savedelit' in request.POST:
                form = DelitsplusForm(request.POST, prefix='delit')
                libe_form = LiberationForm(prefix='libe')
                if form.is_valid():
                    delit = form.save(commit=False)
                    delit.RA = request.user
                    delit.personnegrc = personne
                    delit.province = personne.province
                    delit.nouveaudelit = 1
                    delit.save()
                    messages.success(request, "Les delits du # " + str(personne.codeGRC) + " ont été mis à jour.")
                    if 'Savequit' in request.POST:
                        return redirect(listentp1personne, personne.province_id)
                    else:
                        return redirect(personnentp1delits, personne.id)
        if not libe_form.is_valid():
            messages.error(request, "Il y a une erreur dans l'enregistrement de la liberation")
        if not form.is_valid():
            messages.error(request, "Il y a une erreur dans l'enregistrement du delit")
    return render(request, "personnentp1delits.html", {'personne': personne,
                                                    'delits': delits,
                                                    'liberations': liberations,
                                                    'form': form,
                                                    'libe_form': libe_form,
                                                    'entete' : entete})


## Pour clore les dossiers terminés
@login_required(login_url=settings.LOGIN_URI)
def personnetp1ferme(request, pk):
    personne = Personnegrc.objects.get(pk=pk)
    personne.ferme = 1
    personne.save()
    messages.success(request, "Fermeture de " + str(personne.codeGRC))
    return redirect('listentp1personne', personne.province_id)


