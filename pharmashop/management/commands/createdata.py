
from faker import Faker

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Command information"
    
    # Création des instructions qui vont s'exécuter à l'appel de la  commande """python manage.py createdata"""
    # createdata.py est un fichier que nous devons creer dans le dossier management de l'application
    
    
    def handle(self, *args, **kwargs):
        print("Execution des commande...")
        
        fake = Faker(["fr_FR"])
        print(fake.address())