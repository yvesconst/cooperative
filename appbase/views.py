from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.forms import ModelForm
import json
import re
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from . import models
from django.db import transaction
from .models import *
from django.contrib import messages
from django.conf import settings
import random
from django.core.mail import send_mail
import os
import time
import datetime
from django.core import serializers
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.template.defaultfilters import filesizeformat
from .forms import RegisterForm, ClientForm, CompteFormClient, CompteFormBank, VersementForm, AgenceForm, CaisseForm, PosteForm
from django.db import IntegrityError
from django.core.paginator import Paginator
import traceback

def loginuser(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('appbase:dashboard')
            else:
                return render(request, 'appbase/pages/login.html', {'error_message': 'Votre compte a été désactivé', 'title': 'Connexion', 'color_msg': '#ffc107'})
        else:
            return render(request, 'appbase/login.html', {'error_message': 'Paramètres Invalides', 'title': 'Connexion', 'color_msg': '#dc3545'})
    return render(request, 'appbase/login.html', {'title': 'Connexion'})

def logout_user(request):
	logout(request)
	return redirect('appbase:login')

def lock_user(request):
	username = request.user.username
	logout(request)
	return render(request, 'appbase/lock.html', {'title': 'Connexion', 'username': username})

def register(request):
	employePost = Employe.objects.get(user_id=request.user.id)
	postes = Poste.objects.all()
	if request.method == "POST":
		MyRegisterForm = RegisterForm(request.POST, request.FILES)
		if MyRegisterForm.is_valid():
			try:
				username = MyRegisterForm.cleaned_data["username"]
				password = MyRegisterForm.cleaned_data["password1"]
				passwordConfirm = MyRegisterForm.cleaned_data["password2"]
				if password != passwordConfirm:
					return render(request, 'appbase/register.html', {'title': 'Création d\'un employé', 'postes': postes, 'message_confirm': 'Veuillez écrire le même mot de passe', 'color_msg': '#ffc107'})
				email = MyRegisterForm.cleaned_data["email"]
				user1 = User.objects.create_user(username, email, password)
			except IntegrityError:
				return render(request, 'appbase/register.html', {'title': 'Création d\'un employé', 'postes': postes, 'message_confirm': 'L\'utilisateur existe déjà', 'color_msg': '#dc3545'})
			try:
				employe = Employe()
				idposte = MyRegisterForm.cleaned_data["poste"]
				poste = Poste.objects.get(pk=idposte)
				employe.matricule = MyRegisterForm.cleaned_data["matricule"]
				employe.nom = MyRegisterForm.cleaned_data["nom"]
				employe.prenom = MyRegisterForm.cleaned_data["prenom"]
				employe.adresse = MyRegisterForm.cleaned_data["adresse"]
				employe.tel = MyRegisterForm.cleaned_data["tel"]
				employe.poste = poste
				employe.profil = MyRegisterForm.cleaned_data["profil"]
				employe.photo = MyRegisterForm.cleaned_data["photo"]
				employe.user = user1
				employe.save()
				return render(request, 'appbase/register.html', {'title': 'Création d\'un employé', 'postes': postes, 'message_confirm': 'Utilisateur créé avec succès', 'color_msg': '#28a745', 'employe': employePost})
			except IntegrityError:
				user1.delete()
				return render(request, 'appbase/register.html', {'title': 'Création d\'un employé', 'postes': postes, 'message_confirm': 'Un employé avec le ce numéro de matricule existe déjà', 'color_msg': '#dc3545', 'employe': employePost})
			except NameError:
				user1.delete()
				return render(request, 'appbase/register.html', {'title': 'Création d\'un employé', 'postes': postes, 'message_confirm': 'Le poste n\'existe plus', 'color_msg': '#dc3545', 'employe': employePost})
			except:
				user1.delete()
				return render(request, 'appbase/register.html', {'title': 'Création d\'un employé', 'postes': postes, 'message_confirm': 'Erreur de création', 'color_msg': '#dc3545', 'employe': employePost})
		else:
			return render(request, 'appbase/register.html', {'title': 'Création d\'un employé', 'postes': postes, 'message_confirm': 'Veuillez remplir tous les champs', 'color_msg': '#ffc107', 'employe': employePost})
	return render(request, 'appbase/register.html', {'title': 'Création d\'un employé', 'postes': postes, 'employe': employePost})

def dashboard(request):
	employe = Employe.objects.get(user_id=request.user.id)
	return render(request, 'appbase/dashboard.html', {'title': 'Tableau de bord', 'employe': employe, 'userid': request.user.id})

def employeslist(request, page):
	employe = Employe.objects.get(user_id=request.user.id)
	employes = Employe.objects.all()
	paginator = Paginator(employes, settings.DEFAULT_ITEMS_PER_PAGE)
	page_number = page
	if page_number is not None:
		page_obj = paginator.get_page(page_number)
		return render(request, 'appbase/employes.html', {'title': 'Liste des employés', 'employe': employe, 'userid': request.user.id, 'employes': page_obj})
	page_obj1 = paginator.get_page(1)
	return render(request, 'appbase/employes.html', {'title': 'Liste des employés', 'employe': employe, 'userid': request.user.id, 'employes': page_obj1})

def employeslistfilter(request):
	employe = Employe.objects.get(user_id=request.user.id)
	filterval = request.GET.get('searchitems')
	if filterval is not None:
		employes = Employe.objects.filter(Q(matricule=filterval) | Q(nom=filterval) | Q(prenom=filterval) | Q(adresse=filterval))
		paginator = Paginator(employes, settings.DEFAULT_ITEMS_PER_PAGE)
		page_obj = paginator.get_page(1)
		return render(request, 'appbase/employes.html', {'title': 'Liste des employés', 'employe': employe, 'userid': request.user.id, 'employes': page_obj})
	#employeslist(request, 1)

def clientslist(request, page):
	employe = Employe.objects.get(user_id=request.user.id)
	clients = Client.objects.all()
	paginator = Paginator(clients, settings.DEFAULT_ITEMS_PER_PAGE)
	page_number = page
	if page_number is not None:
		page_obj = paginator.get_page(page_number)
		return render(request, 'appbase/clients.html', {'title': 'Liste des clients', 'employe': employe, 'clients': page_obj})
	page_obj1 = paginator.get_page(1)
	return render(request, 'appbase/clients.html', {'title': 'Liste des clients', 'employe': employe, 'clients': page_obj1})

def createclient(request):
	employePost = Employe.objects.get(user_id=request.user.id)
	if request.method == "POST":
		MyClientForm = ClientForm(request.POST, request.FILES)
		if MyClientForm.is_valid():
			try:
				client = Client()
				client.code = MyClientForm.cleaned_data["code"]
				client.nom = MyClientForm.cleaned_data["nom"]
				client.prenom = MyClientForm.cleaned_data["prenom"]
				client.adresse = MyClientForm.cleaned_data["adresse"]
				client.tel = MyClientForm.cleaned_data["tel"]
				client.cni = MyClientForm.cleaned_data["cni"]
				client.civilite = MyClientForm.cleaned_data["civilite"]
				client.photo = MyClientForm.cleaned_data["photo"]
				client.signature = MyClientForm.cleaned_data["signatureclient"]
				client.nationalite = MyClientForm.cleaned_data["nationalite"]
				client.datenaissance = MyClientForm.cleaned_data["datenaissance"]
				client.profession = MyClientForm.cleaned_data["datenaissance"]
				client.save()
				return render(request, 'appbase/createclient.html', {'title': 'Création d\'un client', 'message_confirm': 'Client créé avec succès', 'color_msg': '#28a745', 'employe': employePost})
			except IntegrityError:
				return render(request, 'appbase/createclient.html', {'title': 'Création d\'un client', 'message_confirm': 'Un client avec le ce numéro de matricule existe déjà', 'color_msg': '#dc3545', 'employe': employePost})
			except NameError:
				return render(request, 'appbase/createclient.html', {'title': 'Création d\'un client', 'message_confirm': 'Le client n\'existe plus', 'color_msg': '#dc3545', 'employe': employePost})
			except:
				return render(request, 'appbase/createclient.html', {'title': 'Création d\'un client', 'message_confirm': 'Erreur de création', 'color_msg': '#dc3545', 'employe': employePost})
		else:
			return render(request, 'appbase/createclient.html', {'title': 'Création d\'un client', 'message_confirm': 'Veuillez remplir tous les champs', 'color_msg': '#ffc107', 'employe': employePost})
	return render(request, 'appbase/createclient.html', {'title': 'Création d\'un client', 'employe': employePost})

def createagence(request):
	employePost = Employe.objects.get(user_id=request.user.id)
	if request.method == "POST":
		MyAgenceForm = AgenceForm(request.POST, request.FILES)
		if MyAgenceForm.is_valid():
			try:
				agence = Agence()
				agence.code = MyAgenceForm.cleaned_data["code"]
				agence.societe = MyAgenceForm.cleaned_data["societe"]
				agence.nom = MyAgenceForm.cleaned_data["nom"]
				agence.adresse = MyAgenceForm.cleaned_data["adresse"]
				agence.tel = MyAgenceForm.cleaned_data["tel"]
				agence.save()
				return render(request, 'appbase/createagence.html', {'title': 'Création d\'une agence', 'message_confirm': 'agence créé avec succès', 'color_msg': '#28a745', 'employe': employePost})
			except IntegrityError:
				return render(request, 'appbase/createagence.html', {'title': 'Création d\'une agence', 'message_confirm': 'Une agence avec le ce numéro de matricule existe déjà', 'color_msg': '#dc3545', 'employe': employePost})
			except NameError:
				return render(request, 'appbase/createagence.html', {'title': 'Création d\'une agence', 'message_confirm': 'L\'agence n\'existe plus', 'color_msg': '#dc3545', 'employe': employePost})
			except:
				return render(request, 'appbase/createagence.html', {'title': 'Création d\'une agence', 'message_confirm': 'Erreur de création', 'color_msg': '#dc3545', 'employe': employePost})
		else:
			return render(request, 'appbase/createagence.html', {'title': 'Création d\'une agence', 'message_confirm': 'Veuillez remplir tous les champs', 'color_msg': '#ffc107', 'employe': employePost})
	return render(request, 'appbase/createagence.html', {'title': 'Création d\'une agence', 'employe': employePost})

def createcaisse(request):
	employePost = Employe.objects.get(user_id=request.user.id)
	agences = Agence.objects.all()
	if request.method == "POST":
		MyCaisseForm = CaisseForm(request.POST, request.FILES)
		if MyCaisseForm.is_valid():
			try:
				caisse = Caisse()
				caisse.code = MyCaisseForm.cleaned_data["code"]
				caisse.libelle = MyCaisseForm.cleaned_data["libelle"]
				agenceid = MyCaisseForm.cleaned_data["agence"]
				agence = Agence.objects.get(pk=agenceid)
				caisse.agence = agence
				caisse.typecaisse = MyCaisseForm.cleaned_data["typecaisse"]
				caisse.save()
				return render(request, 'appbase/createcaisse.html', {'title': 'Création d\'une caisse', 'message_confirm': 'caisse créé avec succès', 'color_msg': '#28a745', 'employe': employePost, 'agences': agences})
			except IntegrityError:
				return render(request, 'appbase/createcaisse.html', {'title': 'Création d\'une caisse', 'message_confirm': 'Une caisse avec le ce numéro de matricule existe déjà', 'color_msg': '#dc3545', 'employe': employePost, 'agences': agences})
			except NameError:
				return render(request, 'appbase/createcaisse.html', {'title': 'Création d\'une caisse', 'message_confirm': 'L\'caisse n\'existe plus', 'color_msg': '#dc3545', 'employe': employePost, 'agences': agences})
			except:
				return render(request, 'appbase/createcaisse.html', {'title': 'Création d\'une caisse', 'message_confirm': 'Erreur de création', 'color_msg': '#dc3545', 'employe': employePost, 'agences': agences})
		else:
			return render(request, 'appbase/createcaisse.html', {'title': 'Création d\'une caisse', 'message_confirm': 'Veuillez remplir tous les champs', 'color_msg': '#ffc107', 'employe': employePost, 'agences': agences})
	return render(request, 'appbase/createcaisse.html', {'title': 'Création d\'une caisse', 'employe': employePost, 'agences': agences})

def createposte(request):
	employePost = Employe.objects.get(user_id=request.user.id)
	agences = Agence.objects.all()
	if request.method == "POST":
		MyPosteForm = PosteForm(request.POST, request.FILES)
		if MyPosteForm.is_valid():
			try:
				caisse = Caisse()
				caisse.code = MyPosteForm.cleaned_data["code"]
				caisse.libelle = MyPosteForm.cleaned_data["libelle"]
				agenceid = MyPosteForm.cleaned_data["agence"]
				agence = Agence.objects.get(pk=agenceid)
				caisse.agence = agence
				caisse.service = MyPosteForm.cleaned_data["service"]
				caisse.save()
				return render(request, 'appbase/createposte.html', {'title': 'Création d\'un poste', 'message_confirm': 'agence créé avec succès', 'color_msg': '#28a745', 'employe': employePost, 'agences': agences})
			except IntegrityError:
				traceback.print_exc()
				return render(request, 'appbase/createposte.html', {'title': 'Création d\'un poste', 'message_confirm': 'Une agence avec le ce numéro de matricule existe déjà', 'color_msg': '#dc3545', 'employe': employePost, 'agences': agences})
			except NameError:
				traceback.print_exc()
				return render(request, 'appbase/createposte.html', {'title': 'Création d\'un poste', 'message_confirm': 'L\'agence n\'existe plus', 'color_msg': '#dc3545', 'employe': employePost, 'agences': agences})
			except:
				traceback.print_exc()
				return render(request, 'appbase/createposte.html', {'title': 'Création d\'un poste', 'message_confirm': 'Erreur de création', 'color_msg': '#dc3545', 'employe': employePost, 'agences': agences})
		else:
			return render(request, 'appbase/createposte.html', {'title': 'Création d\'un poste', 'message_confirm': 'Veuillez remplir tous les champs', 'color_msg': '#ffc107', 'employe': employePost, 'agences': agences})
	return render(request, 'appbase/createposte.html', {'title': 'Création d\'un poste', 'employe': employePost, 'agences': agences})

def createcompte(request, typecpt):
	cmpt = typecpt
	employePost = Employe.objects.get(user_id=request.user.id)
	agences = Agence.objects.all()
	caisses = Caisse.objects.all()
	clients = Client.objects.all()
	if request.method == "POST":
		if typecpt == "B":
			MyCompteForm = CompteFormBank(request.POST, request.FILES)
			fname = "CompteFormBank"
		else:
			MyCompteForm = CompteFormClient(request.POST, request.FILES)
			fname = "CompteFormClient"
		if MyCompteForm.is_valid():
			try:
				compte = Compte()
				compte.numero = MyCompteForm.cleaned_data["numero"]
				compte.typecompte = MyCompteForm.cleaned_data["typecompte"]
				compte.etat = MyCompteForm.cleaned_data["etat"]
				compte.epargne = MyCompteForm.cleaned_data["epargne"]
				compte.solde = MyCompteForm.cleaned_data["solde"]
				idagence = MyCompteForm.cleaned_data["agence"]
				agence = Agence.objects.get(pk=idagence)
				compte.agence = agence
				compte.save()
				if fname == "CompteFormBank":
					caisseid = MyCompteForm.cleaned_data["caisse"]
					caisse = Caisse.objects.get(pk=caisseid)
					comptecaisse = CompteCaisse()
					comptecaisse.caisse = caisse
					comptecaisse.compte = compte
					comptecaisse.etat = "A"
					comptecaisse.save()
				if fname == "CompteFormClient":
					clientid = MyCompteForm.cleaned_data["client"]
					client = Client.objects.get(pk=clientid)
					clientmandataire = ClientMandataire()
					clientmandataire.client = client
					clientmandataire.compte = compte
					clientmandataire.etat = "A"
					clientmandataire.save()
				return render(request, 'appbase/createcompte.html', {'title': 'Création d\'un compte', 'message_confirm': 'Compte créé avec succès', 'color_msg': '#28a745', 'employe': employePost, 'typecmpt': cmpt, 'agences': agences, 'caisses': caisses, 'clients': clients})
			except IntegrityError:
				return render(request, 'appbase/createcompte.html', {'title': 'Création d\'un compte', 'message_confirm': 'Un compte avec le ce numéro existe déjà', 'color_msg': '#dc3545', 'employe': employePost, 'typecmpt': cmpt, 'agences': agences, 'caisses': caisses, 'clients': clients})
			except NameError:
				return render(request, 'appbase/createcompte.html', {'title': 'Création d\'un compte', 'message_confirm': 'L\'agence n\'existe plus', 'color_msg': '#dc3545', 'employe': employePost, 'typecmpt': cmpt, 'agences': agences, 'caisses': caisses, 'clients': clients})
			except:
				traceback.print_exc()
				return render(request, 'appbase/createcompte.html', {'title': 'Création d\'un compte', 'message_confirm': 'Erreur de création', 'color_msg': '#dc3545', 'employe': employePost, 'typecmpt': cmpt, 'agences': agences, 'caisses': caisses, 'clients': clients})
		else:
			return render(request, 'appbase/createcompte.html', {'title': 'Création d\'un compte', 'message_confirm': 'Veuillez remplir tous les champs', 'color_msg': '#ffc107', 'employe': employePost, 'typecmpt': cmpt, 'agences': agences, 'caisses': caisses, 'clients': clients})
	return render(request, 'appbase/createcompte.html', {'title': 'Création d\'un compte', 'employe': employePost, 'typecmpt': cmpt, 'agences': agences, 'caisses': caisses, 'clients': clients})

def createversement(request, cptecred, action):
	employePost = Employe.objects.get(user_id=request.user.id)
	if action == "B":
		fname = "Retrait"
		act = "D"
		comptes = Compte.objects.filter(typecompte='C')
	else:
		fname = "Versement"
		act = "C"
		comptes = Compte.objects.filter(typecompte='B')
	if request.method == "POST":
		MyCompteForm = VersementForm(request.POST, request.FILES)
		if MyCompteForm.is_valid():
			try:
				ecriturecomptable = EcritureComptable()
				ecriturecomptable.depositaire = MyCompteForm.cleaned_data["depositaire"]
				montantecriture = MyCompteForm.cleaned_data["montant"]
				ecriturecomptable.montant = montantecriture
				ecriturecomptable.motif = MyCompteForm.cleaned_data["motif"]
				idcompte = MyCompteForm.cleaned_data["compte"]
				cptecredit = MyCompteForm.cleaned_data["cptecredit"]
				ecriturecomptable.action = act
				ecriturecomptable.employe = employePost
				print(idcompte)
				print(cptecredit)
				if action == "B":
					clientmandataire = ClientMandataire.objects.filter(compte_id=idcompte)
					comptecaisse = CompteCaisse.objects.filter(compte_id=cptecredit)
					ecriturecomptable.clientmandataire = clientmandataire[0]
					ecriturecomptable.comptecaisse = comptecaisse[0]
					compteclient = clientmandataire[0].compte
					compteclient.solde = float(compteclient.solde) - float(montantecriture)
					comptecaisse = comptecaisse[0].compte
					comptecaisse.solde = float(comptecaisse.solde) + float(montantecriture)
				else:
					clientmandataire = ClientMandataire.objects.filter(compte_id=cptecredit)
					comptecaisse = CompteCaisse.objects.filter(compte_id=idcompte)
					ecriturecomptable.clientmandataire = clientmandataire[0]
					ecriturecomptable.comptecaisse = comptecaisse[0]
					compteclient = clientmandataire[0].compte
					compteclient.solde = float(compteclient.solde) + float(montantecriture)
					comptecaisse = comptecaisse[0].compte
					comptecaisse.solde = float(comptecaisse.solde) - float(montantecriture)
				ecriturecomptable.save()
				compteclient.save()
				comptecaisse.save()
				return render(request, 'appbase/createversement.html', {'title': fname, 'message_confirm': fname + ' a été effectué avec succès', 'color_msg': '#28a745', 'employe': employePost, 'cptecredit': cptecred, 'action': action, 'comptes': comptes})
			except IntegrityError:
				traceback.print_exc()
				return render(request, 'appbase/createversement.html', {'title': fname, 'message_confirm': fname + ' été effectué', 'color_msg': '#dc3545', 'employe': employePost, 'cptecredit': cptecred, 'action': action, 'comptes': comptes})
			except NameError:
				traceback.print_exc()
				return render(request, 'appbase/createversement.html', {'title': fname, 'message_confirm': 'Compte n\'existe plus', 'color_msg': '#dc3545', 'employe': employePost, 'cptecredit': cptecred, 'action': action, 'comptes': comptes})
			except:
				traceback.print_exc()
				return render(request, 'appbase/createversement.html', {'title': fname, 'message_confirm': 'Erreur de création', 'color_msg': '#dc3545', 'employe': employePost, 'cptecredit': cptecred, 'action': action, 'comptes': comptes})
		else:
			return render(request, 'appbase/createversement.html', {'title': fname, 'message_confirm': 'Veuillez remplir tous les champs', 'color_msg': '#ffc107', 'employe': employePost, 'cptecredit': cptecred, 'action': action, 'comptes': comptes})
	return render(request, 'appbase/createversement.html', {'title': fname, 'employe': employePost, 'cptecredit': cptecred, 'action': action, 'comptes': comptes})

def agenceslist(request, page):
	employe = Employe.objects.get(user_id=request.user.id)
	agences = Agence.objects.all()
	paginator = Paginator(agences, settings.DEFAULT_ITEMS_PER_PAGE)
	page_number = page
	if page_number is not None:
		page_obj = paginator.get_page(page_number)
		return render(request, 'appbase/agences.html', {'title': 'Liste des agences', 'employe': employe, 'agences': page_obj})
	page_obj1 = paginator.get_page(1)
	return render(request, 'appbase/agences.html', {'title': 'Liste des agences', 'employe': employe, 'agences': page_obj1})

def posteslist(request, page):
	employe = Employe.objects.get(user_id=request.user.id)
	postes = Poste.objects.all()
	paginator = Paginator(postes, settings.DEFAULT_ITEMS_PER_PAGE)
	page_number = page
	if page_number is not None:
		page_obj = paginator.get_page(page_number)
		return render(request, 'appbase/postes.html', {'title': 'Liste des postes', 'employe': employe, 'postes': page_obj})
	page_obj1 = paginator.get_page(1)
	return render(request, 'appbase/postes.html', {'title': 'Liste des postes', 'employe': employe, 'postes': page_obj1})

def caisseslist(request, page):
	employe = Employe.objects.get(user_id=request.user.id)
	caisses = Caisse.objects.all()
	paginator = Paginator(caisses, settings.DEFAULT_ITEMS_PER_PAGE)
	page_number = page
	if page_number is not None:
		page_obj = paginator.get_page(page_number)
		return render(request, 'appbase/caisses.html', {'title': 'Liste des caisse', 'employe': employe, 'caisses': page_obj})
	page_obj1 = paginator.get_page(1)
	return render(request, 'appbase/caisses.html', {'title': 'Liste des caisse', 'employe': employe, 'caisses': page_obj1})

def compteslist(request, page, tcpt):
	listcpmt = []
	if int(tcpt) == 1:
		cmpt = "B"
		comptecaisse = CompteCaisse.objects.all()
		for cc in comptecaisse:
			item = {'caisse': cc.caisse.libelle, 'numero': cc.compte.numero, 'agence': cc.compte.agence.nom, 'typecompte': cc.compte.typecompte, 'etat': cc.compte.etat}
			listcpmt.append(item)
	else:
		cmpt = "C"
		clientmandataire = ClientMandataire.objects.all()
		for cm in clientmandataire:
			item = {'caisse': cm.client.nom, 'numero': cm.compte.numero, 'agence': cm.compte.agence.nom, 'typecompte': cm.compte.typecompte, 'etat': cm.compte.etat}
			listcpmt.append(item)
	employe = Employe.objects.get(user_id=request.user.id)
	#comptes = Compte.objects.filter(typecompte=cmpt)
	#paginator = Paginator(comptes, settings.DEFAULT_ITEMS_PER_PAGE)
	paginator = Paginator(listcpmt, settings.DEFAULT_ITEMS_PER_PAGE)
	page_number = page
	if page_number is not None:
		page_obj = paginator.get_page(page_number)
		return render(request, 'appbase/comptes.html', {'title': 'Liste des comptes', 'employe': employe, 'comptes': page_obj, 'typecmpt': cmpt})
	page_obj1 = paginator.get_page(1)
	return render(request, 'appbase/comptes.html', {'title': 'Liste des comptes', 'employe': employe, 'comptes': page_obj1, 'typecmpt': cmpt})

def versementlist(request, page, action):
	employe = Employe.objects.get(user_id=request.user.id)
	#clients = Client.objects.all()
	listcpmt = []
	if int(action) == 1:
		cmpt = "B"
		namepage = "Retraits"
		comptecaisse = CompteCaisse.objects.all()
		for cc in comptecaisse:
			item = {'id': cc.compte.id, 'caisse': cc.caisse.libelle, 'numero': cc.compte.numero, 'agence': cc.compte.agence.nom, 'typecompte': cc.compte.typecompte, 'etat': cc.compte.etat}
			listcpmt.append(item)
	else:
		cmpt = "C"
		namepage = "Versements"
		clientmandataire = ClientMandataire.objects.all()
		for cm in clientmandataire:
			item = {'id': cm.compte.id, 'caisse': cm.client.nom, 'numero': cm.compte.numero, 'agence': cm.compte.agence.nom, 'typecompte': cm.compte.typecompte, 'etat': cm.compte.etat}
			listcpmt.append(item)
	paginator = Paginator(listcpmt, settings.DEFAULT_ITEMS_PER_PAGE)
	page_number = page
	if page_number is not None:
		page_obj = paginator.get_page(page_number)
		return render(request, 'appbase/versements.html', {'title': namepage, 'employe': employe, 'comptes': page_obj, 'typecmpt': cmpt})
	page_obj1 = paginator.get_page(1)
	return render(request, 'appbase/versements.html', {'title': namepage, 'employe': employe, 'comptes': page_obj1, 'typecmpt': cmpt})

def pretslist(request, page):
	employe = Employe.objects.get(user_id=request.user.id)
	prets = Pret.objects.all()
	paginator = Paginator(prets, settings.DEFAULT_ITEMS_PER_PAGE)
	page_number = page
	if page_number is not None:
		page_obj = paginator.get_page(page_number)
		return render(request, 'appbase/prets.html', {'title': 'Liste des prêts octroyés', 'employe': employe, 'prets': page_obj})
	page_obj1 = paginator.get_page(1)
	return render(request, 'appbase/prets.html', {'title': 'Liste des prêts octroyés', 'employe': employe, 'prets': page_obj1})

def historiques(request, page):
	employe = Employe.objects.get(user_id=request.user.id)
	ecriturecomptables = EcritureComptable.objects.all()
	paginator = Paginator(ecriturecomptables, settings.DEFAULT_ITEMS_PER_PAGE)
	page_number = page
	if page_number is not None:
		page_obj = paginator.get_page(page_number)
		return render(request, 'appbase/historiques.html', {'title': 'Historiques des opérations', 'employe': employe, 'userid': request.user.id, 'ecriturecomptables': page_obj})
	page_obj1 = paginator.get_page(1)
	return render(request, 'appbase/historiques.html', {'title': 'Historiques des opérations', 'employe': employe, 'userid': request.user.id, 'ecriturecomptables': page_obj1})

#def reglementslist(request, page):
#	employe = Employe.objects.get(user_id=request.user.id)
#	reglements = Reglement.objects.all()
#	paginator = Paginator(reglements, settings.DEFAULT_ITEMS_PER_PAGE)
#	page_number = page
#	if page_number is not None:
#		page_obj = paginator.get_page(page_number)
#		return render(request, 'appbase/reglements.html', {'title': 'Liste des règlements', 'employe': employe, 'reglements': page_obj})
#	page_obj1 = paginator.get_page(1)
#	return render(request, 'appbase/reglements.html', {'title': 'Liste des règlements', 'employe': employe, 'reglements': page_obj1})