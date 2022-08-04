# Generated by Django 4.0.5 on 2022-07-05 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmashop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicament',
            name='prix',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='medicament',
            name='qte_stock',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='utilisateur',
            name='adresse',
            field=models.CharField(default='ras', max_length=255),
        ),
    ]