from django.db import models
from django.contrib.auth.models import User
import datetime

class Agence(models.Model):
	id = models.AutoField(primary_key=True)
	societe = models.CharField(max_length=20, blank=True, verbose_name="Societe")
	code = models.CharField(max_length=100, blank=True, verbose_name="Code")
	nom = models.CharField(max_length=100, blank=True, verbose_name="Nom")
	adresse = models.TextField(max_length=30, blank=True, verbose_name="Adresse")
	tel = models.CharField(max_length=500, blank=True, verbose_name="Téléphone")
	Date_creation =  models.DateTimeField(default=datetime.datetime.now)

class Poste(models.Model):
	id = models.AutoField(primary_key=True)
	code = models.CharField(max_length=100, blank=True, verbose_name="Code")
	libelle = models.TextField(max_length=30, blank=True, verbose_name="Libelle")
	service = models.CharField(max_length=100, blank=True, verbose_name="Service")
	agence = models.ForeignKey(
		Agence,
		models.SET_NULL,
		blank=True,
		null=True,
	)
	Date_creation =  models.DateTimeField(default=datetime.datetime.now)

class Employe(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	matricule = models.CharField(max_length=50, blank=True, verbose_name="Matricule")
	nom = models.CharField(max_length=100, blank=True, verbose_name="Nom")
	prenom = models.CharField(max_length=100, blank=True, verbose_name="Prénom")
	adresse = models.TextField(max_length=30, blank=True, verbose_name="Adresse")
	tel = models.CharField(max_length=500, blank=True, verbose_name="Téléphone")
	poste = models.ForeignKey(
		Poste,
		models.SET_NULL,
		blank=True,
		null=True,
	)
	typeprofil = (
		('A', "Administrateur"),
		('C', 'Caissier'),
		('D', "Chef d\'agence"),
	)
	typeetatempl = (
		('A', "Actif"),
		('I', 'Inactif'),
	)
	profil = models.CharField(max_length=1, choices=typeprofil, verbose_name="Profil")
	photo = models.ImageField(upload_to='profils', verbose_name="Photo de profil", blank=True)
	etat = models.CharField(max_length=1, choices=typeetatempl, verbose_name="Etat", default='')
	Date_creation =  models.DateTimeField(default=datetime.datetime.now)

class Client(models.Model):
	id = models.AutoField(primary_key=True)
	code = models.CharField(max_length=50, blank=True, verbose_name="code")
	cni = models.CharField(max_length=30, blank=True, verbose_name="CNI")
	nom = models.CharField(max_length=100, blank=True, verbose_name="Nom")
	prenom = models.CharField(max_length=100, blank=True, verbose_name="Prénom")
	adresse = models.TextField(max_length=30, blank=True, verbose_name="Adresse")
	tel = models.CharField(max_length=500, blank=True, verbose_name="Téléphone")
	profession = models.CharField(max_length=30, blank=True, verbose_name="Profession")
	typeciv = (
		('M', "M."),
		('F', 'Me'),
		('N', 'Mlle'),
	)
	civilite = models.CharField(max_length=1, choices=typeciv, verbose_name="Profil")
	nationalite = models.CharField(max_length=30, blank=True, verbose_name="Nationalité")
	photo = models.ImageField(upload_to='clients', verbose_name="Photo de profil", blank=True)
	signature = models.ImageField(upload_to='signatures', verbose_name="Signature", blank=True)
	datenaissance =  models.DateTimeField(default=datetime.datetime.now)
	Date_creation =  models.DateTimeField(default=datetime.datetime.now)

class Mantataire(models.Model):
	id = models.AutoField(primary_key=True)
	nom = models.CharField(max_length=100, blank=True, verbose_name="Nom")
	prenom = models.CharField(max_length=100, blank=True, verbose_name="Prénom")
	adresse = models.TextField(max_length=30, blank=True, verbose_name="Adresse")
	tel = models.CharField(max_length=500, blank=True, verbose_name="Téléphone")
	Date_creation =  models.DateTimeField(default=datetime.datetime.now)

class Notification(models.Model):
	id = models.AutoField(primary_key=True)
	code = models.CharField(max_length=20, verbose_name="Code", default='')
	description = models.TextField(blank=True, verbose_name="Description")
	user = models.ForeignKey(
		User,
		models.SET_NULL,
		blank=True,
		null=True,
	)
	Date_creation =  models.DateTimeField(default=datetime.datetime.now)
	icon = models.CharField(max_length=20, default='fa fa-arrow-up fa-fw')

class Caisse(models.Model):
	id = models.AutoField(primary_key=True)
	code = models.CharField(max_length=100, blank=True, verbose_name="Code")
	libelle = models.TextField(max_length=30, blank=True, verbose_name="Libelle")
	agence = models.ForeignKey(
		Agence,
		models.SET_NULL,
		blank=True,
		null=True,
	)
	typecaisse1 = (
		('E', "Entreprise"),
		('C', 'Client'),
	)
	typecaisse = models.CharField(max_length=1, choices=typecaisse1, verbose_name="Caisse", default='')
	Date_creation =  models.DateTimeField(default=datetime.datetime.now)

class Compte(models.Model):
	id = models.AutoField(primary_key=True)
	numero = models.CharField(max_length=20, verbose_name="Code", default='')
	agence = models.ForeignKey(
		Agence,
		models.SET_NULL,
		blank=True,
		null=True,
	)
	typeetatcpt = (
		('A', "Actif"),
		('I', 'Inactif'),
	)
	typecpt = (
		('B', "Banque"),
		('C', 'Client'),
	)
	typecompte = models.CharField(max_length=1, choices=typecpt, verbose_name="Type")
	etat = models.CharField(max_length=1, choices=typeetatcpt, verbose_name="Etat")
	epargne = models.BooleanField(default=False)
	solde = models.DecimalField(max_digits=20, decimal_places=2, default=0)
	Date_creation =  models.DateTimeField(default=datetime.datetime.now)

class ClientMandataire(models.Model):
	id = models.AutoField(primary_key=True)
	client = models.ForeignKey(
		Client,
		models.SET_NULL,
		blank=True,
		null=True,
	)
	mantataire = models.ForeignKey(
		Mantataire,
		models.SET_NULL,
		blank=True,
		null=True,
	)
	compte = models.ForeignKey(
		Compte,
		models.SET_NULL,
		blank=True,
		null=True,
	)
	typeetat = (
		('A', "Actif"),
		('I', 'Inactif'),
	)
	etat = models.CharField(max_length=1, choices=typeetat, verbose_name="Etat")
	Date_creation =  models.DateTimeField(default=datetime.datetime.now)

class CompteCaisse(models.Model):
	id = models.AutoField(primary_key=True)
	caisse = models.ForeignKey(
		Caisse,
		models.SET_NULL,
		blank=True,
		null=True,
	)
	compte = models.ForeignKey(
		Compte,
		models.SET_NULL,
		blank=True,
		null=True,
	)
	typeetat = (
		('A', "Actif"),
		('I', 'Inactif'),
	)
	etat = models.CharField(max_length=1, choices=typeetat, verbose_name="Etat")
	Date_creation =  models.DateTimeField(default=datetime.datetime.now)

class EcritureComptable(models.Model):
	id = models.AutoField(primary_key=True)
	employe = models.ForeignKey(
		Employe,
		models.SET_NULL,
		blank=True,
		null=True,
	)
	clientmandataire = models.ForeignKey(
		ClientMandataire,
		models.SET_NULL,
		blank=True,
		null=True,
	)
	comptecaisse = models.ForeignKey(
		CompteCaisse,
		models.SET_NULL,
		blank=True,
		null=True,
	)
	typeaction = (
		('C', "Crédit"),
		('D', 'Débit'),
	)
	action = models.CharField(max_length=1, choices=typeaction, verbose_name="Etat")
	depositaire = models.CharField(max_length=100, blank=True, verbose_name="Dépositaire")
	motif = models.CharField(max_length=100, blank=True, verbose_name="Motif")
	montant = models.DecimalField(max_digits=20, decimal_places=2)
	Date_creation =  models.DateTimeField(default=datetime.datetime.now)

class Pret(models.Model):
	id = models.AutoField(primary_key=True)
	clientmandataire = models.ForeignKey(
		ClientMandataire,
		models.SET_NULL,
		blank=True,
		null=True,
	)
	montant = models.DecimalField(max_digits=20, decimal_places=2)
	interet = models.DecimalField(max_digits=20, decimal_places=2)
	penalite = models.DecimalField(max_digits=20, decimal_places=2)
	motif_pret = models.CharField(max_length=100, blank=True, verbose_name="Motif")
	Date_acquisition =  models.DateTimeField(default=datetime.datetime.now)

class DetailPret(models.Model):
	id = models.AutoField(primary_key=True)
	pret = models.ForeignKey(
		Pret,
		models.SET_NULL,
		blank=True,
		null=True,
	)
	dotation = models.DecimalField(max_digits=20, decimal_places=2)
	reste = models.DecimalField(max_digits=20, decimal_places=2)
	Date_versement =  models.DateTimeField(default=datetime.datetime.now)

class HistoOperation(models.Model):
	id = models.AutoField(primary_key=True)
	employe = models.ForeignKey(
		Employe,
		models.SET_NULL,
		blank=True,
		null=True,
	)
	compte = models.ForeignKey(
		Compte,
		models.SET_NULL,
		blank=True,
		null=True,
	)
	motif = models.CharField(max_length=255, blank=True, verbose_name="Motif")
	action = models.CharField(max_length=100, blank=True, verbose_name="Motif")
	Date_modification =  models.DateTimeField(default=datetime.datetime.now)