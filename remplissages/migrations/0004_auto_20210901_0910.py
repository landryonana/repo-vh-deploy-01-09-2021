# Generated by Django 2.2.24 on 2021-09-01 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('remplissages', '0003_auto_20210831_1627'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='nom_et_prenom',
            field=models.CharField(error_messages={'unique': 'Une personne avec ce nom existe déjà'}, help_text='ce champ doit avoir au moins trois caractères', max_length=200, unique=True, verbose_name='Nom et Prénom'),
        ),
    ]