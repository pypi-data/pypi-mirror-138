from django.db import models
from djangoldp.models import Model

class Member(Model):
    name = models.CharField(max_length=25, blank=True, null=True, verbose_name="Nom")
    picture = models.ImageField(blank=True, null=True, verbose_name="Photo")
    title = models.CharField(blank=True, null=True, max_length=25, verbose_name="métier")
    society = models.CharField(blank=True, null=True, max_length=50, verbose_name="société")

    def __str__(self):
        return self.name

class Partnertype(Model):
    name = models.CharField(max_length=25, blank=True, null=True, verbose_name="Type de partenariat")

    def __str__(self):
        return self.name

class Partner(Model):
    name = models.CharField(max_length=25, blank=True, null=True, verbose_name="Nom du partenaire")
    illustration = models.ImageField(blank=True, null=True, verbose_name="illustration")
    logo = models.ImageField(blank=True, null=True, verbose_name="logo")
    partnertype = models.ForeignKey(Partnertype, blank=True, null=True, on_delete=models.SET_NULL, verbose_name="type de partenaire")
    presentation = models.CharField(max_length=100, blank=True, null=True, verbose_name="courte présentation du partenaire" )
    offer = models.CharField(max_length=100, blank=True, null=True, verbose_name="présentation de l'offre")
    offerlink = models.URLField(blank=True, null=True, verbose_name="Lien vers l'offre")

    def __str__(self):
        return self.name

class Project(Model):
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nom du projet")
    img = models.ImageField(blank=True, null=True, verbose_name="Illustration du projet")
    presentation = models.CharField(max_length=250, blank=True, null=True, verbose_name="Présentation du projet" )
    visible = models.BooleanField(verbose_name="Visible sur le site", blank=True, null=True,  default=False)

    def __str__(self):
        return self.name
