from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from . import views
from django.views.static import serve
from django.conf import settings

app_name = 'appbase'

urlpatterns = [
	url(r'^$', views.loginuser, name='login'),
    url(r'^register/$', views.register, name='register'),
	url(r'^createclient/$', views.createclient, name='createclient'),
	url(r'^createagence/$', views.createagence, name='createagence'),
	url(r'^createposte/$', views.createposte, name='createposte'),
	url(r'^createcaisse/$', views.createcaisse, name='createcaisse'),
	#url(r'^createcompte/$', views.createcompte, name='createcompte'),
	path('createcompte/<str:typecpt>/', views.createcompte, name='createcompte'),
	path('createversement/<str:cptecred>/<str:action>/', views.createversement, name='createversement'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
	#url(r'^employeslist/$', views.employeslist, name='employeslist'),
	path('employeslist/<str:page>/', views.employeslist, name='employeslist'),
	path('employeslistfilter/', views.employeslistfilter, name='employeslistfilter'),
	path('posteslist/<str:page>/', views.posteslist, name='posteslist'),
	path('agenceslist/<str:page>/', views.agenceslist, name='agenceslist'),
	path('caisseslist/<str:page>/', views.caisseslist, name='caisseslist'),
	path('clientslist/<str:page>/', views.clientslist, name='clientslist'),
	path('compteslist/<str:page>/<str:tcpt>/', views.compteslist, name='compteslist'),
	path('pretslist/<str:page>/', views.pretslist, name='pretslist'),
	path('versementlist/<str:page>/<str:action>/', views.versementlist, name='versementlist'),
	path('historiques/<str:page>/', views.historiques, name='historiques'),
	
    url(r'^déconnexion/$', views.logout_user, name='logout'),
	url(r'^lock/$', views.lock_user, name='lock'),
    url(r'^media/(?P<path>.*)$', serve, { 'document_root': settings.MEDIA_ROOT}),
]