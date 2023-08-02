
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
        
        pharmacies = []
        entrepots = []
        categories = []
        
        nombre = 15
        
        
        for _ in range(int(nombre/3)):
            categorie = models.Categorie.objects.create(
                libelle=fake.unique.text(max_nb_chars=15),
            )
            categories.append(categorie)
        count = 1
        
        while count <= 15:
            # Création des utilisateurs
            try:
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
                count += 1
            except:
                print("Existing user")
           
            
        for _ in range(nombre):
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
                user = models.Utilisateur.objects.get(id=fake.random_int(1, nombre))
            )
            
            pharmacies.append(pharmacie)
            
        for _ in range(nombre):
            # Création d'entrepôt 
            entrepot = models.Entrepot.objects.create(
                nom = fake.text(max_nb_chars=10),
                pays = fake.text(max_nb_chars=10),
                ville = fake.text(max_nb_chars=10),
                telephone = fake.unique.phone_number(),
                description = fake.unique.text(max_nb_chars=100),
                pharmacie = pharmacies[fake.random_int(0, nombre - 1)],
            )
            entrepots.append(entrepot)
            
        for _ in range(nombre):
             # Création de quelques médicaments
            medicament = models.Medicament.objects.create(
                nom = fake.text(max_nb_chars=10),
                prix = fake.random_int(200, 10000),
                marque = fake.company(),
                date_exp = fake.iso8601(),
                masse = "{}g".format(fake.random_int(0, 500)),
                qte_stock = fake.random_int(0, 1000),
                stockAlert = fake.random_int(10, 1000),
                stockOptimal = fake.random_int(20, 1000),
                description = fake.unique.text(max_nb_chars=100),
                posologie = fake.unique.text(max_nb_chars=100),
                voix = fake.random_int(0, 2),
                categorie = categories[fake.random_int(0, (int(nombre/3) - 1))],
                user = models.Utilisateur.objects.get(id=fake.random_int(1, nombre )),
                pharmacie = pharmacies[fake.random_int(0, nombre - 1)],
                entrepot = entrepots[fake.random_int(0, nombre - 1)]
            )
          
            
        print(models.User.objects.all().count())
        print(models.Pharmacie.objects.all().count())