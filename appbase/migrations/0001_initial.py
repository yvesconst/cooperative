# Generated by Django 3.0.3 on 2020-02-12 16:01

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Agence',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('societe', models.CharField(blank=True, max_length=20, verbose_name='code')),
                ('code', models.CharField(blank=True, max_length=100, verbose_name='Code')),
                ('nom', models.CharField(blank=True, max_length=100, verbose_name='Prénom')),
                ('adresse', models.TextField(blank=True, max_length=30, verbose_name='Adresse')),
                ('tel', models.CharField(blank=True, max_length=500, verbose_name='Téléphone')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(blank=True, max_length=50, verbose_name='code')),
                ('cni', models.CharField(blank=True, max_length=30, verbose_name='CNI')),
                ('nom', models.CharField(blank=True, max_length=100, verbose_name='Nom')),
                ('prenom', models.CharField(blank=True, max_length=100, verbose_name='Prénom')),
                ('adresse', models.TextField(blank=True, max_length=30, verbose_name='Adresse')),
                ('tel', models.CharField(blank=True, max_length=500, verbose_name='Téléphone')),
                ('profession', models.CharField(blank=True, max_length=30, verbose_name='Profession')),
                ('civilite', models.CharField(choices=[('H', 'M.'), ('F', 'Me')], max_length=1, verbose_name='Profil')),
                ('nationalite', models.CharField(blank=True, max_length=30, verbose_name='Nationalité')),
                ('photo', models.ImageField(blank=True, upload_to='profils', verbose_name='Photo de profil')),
                ('signature', models.ImageField(blank=True, upload_to='signatures', verbose_name='Signature')),
                ('datenaissance', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='ClientMandataire',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('etat', models.CharField(choices=[('A', 'Actif'), ('I', 'Inactif')], max_length=1, verbose_name='Etat')),
                ('Date_creation', models.DateTimeField(default=datetime.datetime.now)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='appbase.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Compte',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('numero', models.CharField(default='', max_length=20, verbose_name='Code')),
                ('typecompte', models.CharField(choices=[('P', 'Particulier'), ('E', 'Entreprise'), ('S', 'Societé')], max_length=1, verbose_name='Type')),
                ('etat', models.CharField(choices=[('A', 'Actif'), ('I', 'Inactif')], max_length=1, verbose_name='Etat')),
                ('Date_creation', models.DateTimeField(default=datetime.datetime.now)),
                ('agence', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='appbase.Agence')),
            ],
        ),
        migrations.CreateModel(
            name='Employe',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('matricule', models.CharField(blank=True, max_length=50, verbose_name='Matricule')),
                ('nom', models.CharField(blank=True, max_length=100, verbose_name='Nom')),
                ('prenom', models.CharField(blank=True, max_length=100, verbose_name='Prénom')),
                ('adresse', models.TextField(blank=True, max_length=30, verbose_name='Adresse')),
                ('tel', models.CharField(blank=True, max_length=500, verbose_name='Téléphone')),
                ('poste', models.CharField(blank=True, max_length=30, verbose_name='Poste')),
                ('profil', models.CharField(choices=[('A', 'Administrateur'), ('C', 'Caissier'), ('D', "Chef d'agence")], max_length=1, verbose_name='Profil')),
                ('photo', models.ImageField(blank=True, upload_to='profil', verbose_name='Photo de profil')),
                ('agence', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='appbase.Agence')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Mantataire',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(blank=True, max_length=100, verbose_name='Nom')),
                ('prenom', models.CharField(blank=True, max_length=100, verbose_name='Prénom')),
                ('adresse', models.TextField(blank=True, max_length=30, verbose_name='Adresse')),
                ('tel', models.CharField(blank=True, max_length=500, verbose_name='Téléphone')),
            ],
        ),
        migrations.CreateModel(
            name='Reglement',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('typereglement', models.CharField(choices=[('C', 'Cash'), ('V', 'Virement')], max_length=1, verbose_name='Etat')),
                ('depositaire', models.CharField(blank=True, max_length=100, verbose_name='Motif')),
                ('motif', models.CharField(blank=True, max_length=100, verbose_name='Motif')),
                ('Date_reglement', models.DateTimeField(default=datetime.datetime.now)),
                ('employe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='appbase.Employe')),
            ],
        ),
        migrations.CreateModel(
            name='Pret',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('montant', models.DecimalField(decimal_places=2, max_digits=20)),
                ('interet', models.DecimalField(decimal_places=2, max_digits=20)),
                ('penalite', models.DecimalField(decimal_places=2, max_digits=20)),
                ('motif_pret', models.CharField(blank=True, max_length=100, verbose_name='Motif')),
                ('Date_acquisition', models.DateTimeField(default=datetime.datetime.now)),
                ('clientmandataire', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='appbase.ClientMandataire')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('code', models.CharField(default='', max_length=20, verbose_name='Code')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('Date_creation', models.DateTimeField(default=datetime.datetime.now)),
                ('icon', models.CharField(default='fa fa-arrow-up fa-fw', max_length=20)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HistoOperation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('motif', models.CharField(blank=True, max_length=255, verbose_name='Motif')),
                ('action', models.CharField(blank=True, max_length=100, verbose_name='Motif')),
                ('Date_modification', models.DateTimeField(default=datetime.datetime.now)),
                ('compte', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='appbase.Compte')),
                ('employe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='appbase.Employe')),
            ],
        ),
        migrations.CreateModel(
            name='DetailPret',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dotation', models.DecimalField(decimal_places=2, max_digits=20)),
                ('reste', models.DecimalField(decimal_places=2, max_digits=20)),
                ('Date_versement', models.DateTimeField(default=datetime.datetime.now)),
                ('pret', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='appbase.Pret')),
            ],
        ),
        migrations.CreateModel(
            name='DetailCompte',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('action', models.CharField(choices=[('C', 'Crédit'), ('D', 'Débit')], max_length=1, verbose_name='Etat')),
                ('montant', models.DecimalField(decimal_places=2, max_digits=20)),
                ('solde', models.DecimalField(decimal_places=2, max_digits=20)),
                ('Date_creation', models.DateTimeField(default=datetime.datetime.now)),
                ('compte', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='appbase.Compte')),
                ('employe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='appbase.Employe')),
                ('reglement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='appbase.Reglement')),
            ],
        ),
        migrations.AddField(
            model_name='clientmandataire',
            name='compte',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='appbase.Compte'),
        ),
        migrations.AddField(
            model_name='clientmandataire',
            name='mantataire',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='appbase.Mantataire'),
        ),
    ]
