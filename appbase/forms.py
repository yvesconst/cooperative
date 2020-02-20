from django import forms

class RegisterForm(forms.Form):
	email =  forms.EmailField()
	username = forms.CharField(max_length=50)
	password1 = forms.CharField(max_length=50)
	password2 = forms.CharField(max_length=50)
	matricule = forms.CharField(max_length=50)
	nom = forms.CharField(max_length=100)
	prenom = forms.CharField(max_length=100)
	adresse = forms.CharField(max_length=30)
	tel = forms.CharField(max_length=500)
	profil = forms.CharField(max_length=1)
	poste = forms.CharField(max_length=1)
	photo = forms.ImageField()

class AgenceForm(forms.Form):
	code =  forms.CharField(max_length=50)
	societe =  forms.CharField(max_length=50)
	nom = forms.CharField(max_length=100)
	adresse = forms.CharField(max_length=50)
	tel = forms.CharField(max_length=50)

class CaisseForm(forms.Form):
	code =  forms.CharField(max_length=50)
	libelle =  forms.CharField(max_length=50)
	agence = forms.CharField(max_length=50)
	typecaisse = forms.CharField(max_length=1)

class PosteForm(forms.Form):
	code =  forms.CharField(max_length=50)
	libelle =  forms.CharField(max_length=50)
	agence = forms.CharField(max_length=50)
	service = forms.CharField(max_length=50)

class ClientForm(forms.Form):
	code =  forms.CharField(max_length=50)
	profession =  forms.CharField(max_length=50)
	nationalite = forms.CharField(max_length=50)
	cni = forms.CharField(max_length=50)
	datenaissance = forms.DateField()
	nom = forms.CharField(max_length=100)
	prenom = forms.CharField(max_length=100)
	adresse = forms.CharField(max_length=30)
	tel = forms.CharField(max_length=500)
	civilite = forms.CharField(max_length=1)
	photo = forms.ImageField()
	signatureclient = forms.ImageField()

class CompteFormClient(forms.Form):
	numero =  forms.CharField(max_length=50)
	typecompte =  forms.CharField(max_length=1)
	etat = forms.CharField(max_length=1)
	solde = forms.DecimalField(max_digits=20, decimal_places=2, localize=True)
	agence = forms.CharField(max_length=50)
	client = forms.CharField(max_length=50)
	epargne = forms.BooleanField(required=False)

class CompteFormBank(forms.Form):
	numero =  forms.CharField(max_length=50)
	typecompte =  forms.CharField(max_length=1)
	etat = forms.CharField(max_length=1)
	solde = forms.DecimalField(max_digits=20, decimal_places=2, localize=True)
	caisse = forms.CharField(max_length=50)
	agence = forms.CharField(max_length=50)
	epargne = forms.BooleanField(required=False)

class VersementForm(forms.Form):
	depositaire =  forms.CharField(max_length=100)
	montant = forms.DecimalField(max_digits=20, decimal_places=2, localize=True)
	motif = forms.CharField(max_length=250)
	compte = forms.CharField(max_length=50)
	cptecredit = forms.CharField(max_length=50)
	action = forms.CharField(max_length=1)