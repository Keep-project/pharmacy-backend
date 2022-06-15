# Generated by Django 4.0.5 on 2022-06-10 19:20

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categorie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Symptome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('libelle', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('adresse', models.CharField(max_length=255)),
            ],
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Pharmacie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('localisation', models.CharField(max_length=255)),
                ('tel', models.CharField(max_length=255)),
                ('latitude', models.DecimalField(decimal_places=10, max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=10, max_digits=10)),
                ('h_ouverture', models.DateTimeField(null=True)),
                ('h_fermeture', models.DateTimeField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmashop.utilisateur')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Medicament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('prix', models.DecimalField(decimal_places=5, max_digits=10)),
                ('marque', models.CharField(max_length=255)),
                ('date_exp', models.DateTimeField()),
                ('image', models.FileField(upload_to='images/')),
                ('masse', models.CharField(max_length=10)),
                ('qte_stock', models.IntegerField()),
                ('description', models.CharField(max_length=255)),
                ('posologie', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('categorie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medicaments', to='pharmashop.categorie')),
                ('pharmacie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmashop.utilisateur')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='medicaments', to='pharmashop.utilisateur')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Consultaion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('symptome', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmashop.symptome')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmashop.utilisateur')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Carnet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reponse', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('consultation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pharmashop.consultaion')),
            ],
            options={
                'ordering': ('-created_at',),
            },
        ),
    ]
