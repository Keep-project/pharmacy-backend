# Generated by Django 4.0.5 on 2022-08-13 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pharmashop', '0006_mouvementinventaire_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='medicament',
            unique_together={('nom', 'pharmacie')},
        ),
    ]
