# Generated by Django 3.0.3 on 2020-02-18 22:59

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appbase', '0005_auto_20200216_1322'),
    ]

    operations = [
        migrations.CreateModel(
            name='EcritureComptable',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('action', models.CharField(choices=[('C', 'Crédit'), ('D', 'Débit')], max_length=1, verbose_name='Etat')),
                ('depositaire', models.CharField(blank=True, max_length=100, verbose_name='Dépositaire')),
                ('motif', models.CharField(blank=True, max_length=100, verbose_name='Motif')),
                ('montant', models.DecimalField(decimal_places=2, max_digits=20)),
                ('Date_creation', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.RemoveField(
            model_name='reglement',
            name='caisse',
        ),
        migrations.RemoveField(
            model_name='reglement',
            name='employe',
        ),
        migrations.AddField(
            model_name='caisse',
            name='compte',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='appbase.Compte'),
        ),
        migrations.AddField(
            model_name='compte',
            name='epargne',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='compte',
            name='solde',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
        migrations.AlterField(
            model_name='compte',
            name='typecompte',
            field=models.CharField(choices=[('B', 'Banque'), ('C', 'Client')], max_length=1, verbose_name='Type'),
        ),
        migrations.DeleteModel(
            name='DetailCompte',
        ),
        migrations.DeleteModel(
            name='Reglement',
        ),
        migrations.AddField(
            model_name='ecriturecomptable',
            name='caisse',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='appbase.Caisse'),
        ),
        migrations.AddField(
            model_name='ecriturecomptable',
            name='clientmandataire',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='appbase.ClientMandataire'),
        ),
        migrations.AddField(
            model_name='ecriturecomptable',
            name='employe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='appbase.Employe'),
        ),
    ]
