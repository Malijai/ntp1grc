from __future__ import unicode_literals
from django import template
from django.apps import apps
from django import forms

register = template.Library()


@register.simple_tag
def faitvalslangue(table, lang, nom_champ, *args, **kwargs):
    klass = apps.get_model('NTP1Reprise', table)
    #   klass = apps.get_model('dataentry', sortetable[b])
    listevaleurs = klass.objects.all()
    liste = fait_liste_tables(listevaleurs, lang)
    question = forms.Select(choices=liste, attrs={ })
#    question = forms.Select(choices=liste, attrs={'name': table, })
    default = ''
    if table == "Duree" or table == "Type":
        default = '998'
    else:
        default = ''
    return question.render(nom_champ, default)


def fait_liste_tables(listevaleurs, lang):
    liste = [('', '')]
    for valeur in listevaleurs:
        if lang == 'en' or lang == 'EN':
            val = valeur.reponse_valeur
            nen = valeur.reponse_en
            liste.append((val, nen))
        else:
            val = valeur.reponse_valeur
            nen = valeur.reponse_fr
            liste.append((val, nen))
    return liste


