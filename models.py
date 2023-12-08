from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


## Liste des valeurs des choix de
# Code de violation
class Violation(models.Model):
    reponse_valeur = models.CharField(max_length=200)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )

    def __str__(self):
        return '%s %s' % (self.reponse_valeur, self.reponse_en)


## Tribunaux
class Tribunal(models.Model):
    reponse_valeur = models.CharField(max_length=200)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )

    def __str__(self):
        return '%s' % self.reponse_fr

# Verdicts
class Verdict(models.Model):
    reponse_valeur = models.CharField(max_length=200)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )

    def __str__(self):
        return '%s' % self.reponse_fr

# Provinces
class Province(models.Model):
    reponse_en = models.CharField(max_length=30,)
    reponse_fr = models.CharField(max_length=30,)

    def __str__(self):
        return '%s' % self.reponse_fr

# Municipalites par provinces
class Municipalite(models.Model):
    reponse_valeur = models.CharField(max_length=20)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )
    province = models.ForeignKey(Province, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['reponse_fr']

    def __str__(self):
        return '%s' % self.reponse_fr

class Type(models.Model):
    reponse_valeur = models.CharField(max_length=20)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )

    class Meta:
        ordering = ['reponse_fr']

    def __str__(self):
        return '%s' % self.reponse_fr

class Duree(models.Model):
    reponse_valeur = models.CharField(max_length=20)
    reponse_en = models.CharField(max_length=200, )
    reponse_fr = models.CharField(max_length=200, )

    class Meta:
        ordering = ['reponse_valeur']

    def __str__(self):
        return '%s' % self.reponse_fr

## Entrée des données
# Liste de tous les dossiers avec ou sans FPS
class Personnegrc(models.Model):
    codeGRC = models.IntegerField(verbose_name=_("ID"))
    prenom = models.CharField(max_length=200, verbose_name=_("Prénom"))
    province = models.ForeignKey(Province, on_delete=models.DO_NOTHING)
    delit = models.IntegerField(default=1, verbose_name=_("Présence ancien délits"),)
    dateprint1 = models.DateField(verbose_name=_("Ancienne date print"),)
    oldpresencefps = models.IntegerField(verbose_name=_("Présence ancien FPS"),)
    dateprint2 = models.DateField(verbose_name=_("Date print. Laisser vide si pas de fichier."), blank=True, null=True)
    newdelit = models.BooleanField(default=1, verbose_name=_("Présence de délits après la date du dernier verdict rentré"),)
    newpresencefps = models.BooleanField(verbose_name=_("Cocher OUI si présence de dossier ou si dossier -non disclosable-"),)
    confidentiel = models.BooleanField(verbose_name=_("Les données sont elles confidentielles (non disclosable). Cocher si oui"), blank=True, null=True)
    dateverdictder = models.DateField(verbose_name=_("Date du dernier verdict présent dans la fiche. Laisser vide si pas de fichier"), blank=True, null=True)
    ferme = models.BooleanField()
    datedeces = models.DateField(verbose_name=_("Si décédé indiquer la date ici"), blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    RA = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['codeGRC']

    def __str__(self):
        return '%s' % self.codeGRC

# Une fiche pour chaque délit de chaque personne.
class Delitsplus(models.Model):
    personnegrc = models.ForeignKey(Personnegrc, on_delete=models.CASCADE, verbose_name="ID")
    date_sentence = models.DateField(verbose_name=_("Date de la décision (jj/mm/aaaa)"))
    type_tribunal = models.ForeignKey(Tribunal, on_delete=models.DO_NOTHING, verbose_name=_("Type de tribunal"))
    lieu_sentence = models.ForeignKey(Municipalite, on_delete=models.DO_NOTHING, verbose_name=_("Lieu du verdict"))
    ordre_delit = models.IntegerField(default=1, verbose_name=_("Ordre"),)
    descriptiondelit = models.CharField(max_length=150, verbose_name=_("Description du délit"), null=True, blank=True)
    codeCCdelit = models.CharField(max_length=50, verbose_name=_("Code CC du delit (si pas CC preciser de quel code il s agit). Si pas de code mettre Inconnu"))
    nombre_chefs = models.IntegerField(default=1,verbose_name=_("Nombre de chefs"))
    violation = models.ForeignKey(Violation, on_delete=models.DO_NOTHING, verbose_name=_("Code de violation"))
    verdict = models.ForeignKey(Verdict, related_name='verdict', on_delete=models.DO_NOTHING, verbose_name=_("Verdict"))
    amendeON = models.BooleanField(verbose_name=_("Amende, frais etc.? Cocher si oui"))
    amende_type =  models.ForeignKey(Type, default=998, on_delete=models.DO_NOTHING, verbose_name=_("Caractéristiques de l'amende"),null=True, blank=True)
    amendecout = models.IntegerField(default=0,verbose_name=_("Cout total de l'amende (+ surmende + frais + restitution)"), null=True, blank=True)
    detentionON = models.BooleanField(verbose_name=_("Détention? Cocher si oui"))
    detentionduree = models.IntegerField(default=0, verbose_name=_("Durée de la détention (ajouter sentence + présentence)"), null=True, blank=True)
    unitedetention =  models.ForeignKey(Duree, default=998, related_name='duree_detention', on_delete=models.DO_NOTHING, verbose_name=_("Jours, mois, ans etc?"), null=True, blank=True)
    probationON = models.BooleanField(verbose_name=_("Probation? Cocher si oui"))
    probationduree = models.IntegerField(default=0, verbose_name=_("Durée de la probation"), null=True, blank=True)
    uniteprobation =  models.ForeignKey(Duree, default=998, related_name='duree_probation', on_delete=models.DO_NOTHING, verbose_name=_("Jours, mois, ans etc?"), null=True, blank=True)
    interdictionON = models.BooleanField(verbose_name=_("Interdiction? Cocher si oui"))
    interdictionduree = models.IntegerField(default=0, verbose_name=_("Durée de l'interdiction"), null=True, blank=True)
    uniteinterdiction =  models.ForeignKey(Duree, default=998, related_name='duree_interdiction', on_delete=models.DO_NOTHING, verbose_name=_("Jours, mois, ans etc?"), null=True, blank=True)
    interdictiondetails = models.CharField(max_length=150, verbose_name=_("Détails à propos de l'interdiction"), null=True, blank=True)
    surcisON = models.BooleanField(verbose_name=_("Surcis? Cocher si oui"))
    surcisduree = models.IntegerField(default=0, verbose_name=_("Durée du surcis"), null=True, blank=True)
    unitesurcis =  models.ForeignKey(Duree, default=998, related_name='duree_surcis', on_delete=models.DO_NOTHING, verbose_name=_("Jours, mois, ans etc?"), null=True, blank=True)
    autreON = models.BooleanField(verbose_name=_("Autre? Cocher si oui"))
    autredetails = models.CharField(max_length=100, blank=True, null=True,verbose_name=_("Si autre : détails"))
    # consecutifsON = models.BooleanField(verbose_name=_("Consécutif? Cocher si oui"))
    RA = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    card = models.IntegerField(default=1)
    nouveaudelit = models.BooleanField()

    class Meta:
        ordering = ['personnegrc', 'date_sentence', 'ordre_delit']
        unique_together = (('personnegrc', 'date_sentence', 'ordre_delit','RA'),)
        indexes = [models.Index(fields=['personnegrc', 'date_sentence', 'ordre_delit','RA'])]

    def __str__(self):
        return '%s %s %s' % (self.personnegrc, self.date_sentence, self.ordre_delit)

# Une fiche pour chaque liberation de chaque personne.
class Liberation(models.Model):
    personnegrc = models.ForeignKey(Personnegrc, on_delete=models.CASCADE, verbose_name="ID")
    date_liberation = models.DateField(verbose_name=_("Date de la libération"))
    type = models.BooleanField(verbose_name=_("Libération absolue? Cocher si oui"))
    RA = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['personnegrc', 'date_liberation']

    def __str__(self):
        return '%s %s' % (self.personnegrc, self.date_liberation)