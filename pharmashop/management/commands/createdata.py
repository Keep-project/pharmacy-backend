
from faker import Faker
from pharmashop import models
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Command information"
    
    # Création des instructions qui vont s'exécuter à l'appel de la  commande """python manage.py createdata"""
    # createdata.py est un fichier que nous devons creer dans le dossier management de l'application
    
    
    def handle(self, *args, **kwargs):
        print("Execution des commande...")
        
        fake = Faker(["fr_FR"])
        
        
        for i in range(15):
            print("================ {0} ================".format(i))
            # Créattion des utilisateurs
            user = models.Utilisateur.objects.create_user(
                username=fake.unique.first_name(),
                password="patson120",
                adresse=fake.unique.address(),
                email=fake.unique.email(),
                status= fake.unique.text(max_nb_chars=5),
                experience= fake.random_int(0, 40),
                avatar='',
                is_active=True,
                is_staff=True,
                is_superuser=False
            )
            
            # Créattion des Pharmacies
            pharmacie = models.Pharmacie.objects.create(
                libelle=fake.unique.text(max_nb_chars=10),
                nom=fake.unique.company(),
                localisation=fake.unique.address(),
                tel = fake.unique.phone_number(),
                email=fake.unique.email(),
                latitude=fake.unique.latitude(),
                longitude=fake.unique.longitude(),
                h_ouverture = fake.unique.time(pattern = '%H:%M:%S'),
                h_fermeture = fake.unique.time(pattern = '%H:%M:%S'),
                user = user
            )
            
        print(models.User.objects.all().count())
        print(models.Pharmacie.objects.all().count())