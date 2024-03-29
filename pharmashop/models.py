from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q, Sum
import datetime
import uuid


# Create your models here.

#  liste des models
#  -pharmacie
#  -medicament
#  -catégorie
#  -utilisateur
#  -maladie
#  -symptôme
#  -consultation
#  -carnet (portant les informations de la consultation)


class BaseModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


'''BASE_URL = 'http://192.168.162.232:8000'''
'''BASE_URL = 'http://192.168.220.1:8000'''
BASE_URL = 'http://192.168.0.104:8000'
'''BASE_URL = 'https://pocketpharma.herokuapp.com'''

def upload_path(instance, filename):
    date = datetime.datetime.now().timestamp()
    return '/'.join(["images/", '{0}'.format(date) + filename])


class Categorie(BaseModel):
    libelle = models.CharField(max_length=50)

    class Meta:
        '''
            Création de ses propres permissions sur le modèle. 
            Après avoir définit les permissions, il faut toujours faire les migrations
            vers la base de données.
        '''
        permissions = (
            ('publier', 'Peut publier catégorie'),
        )
       
    def __str__(self):
        return "{0}".format(self.libelle)
        

class Utilisateur(User):
    adresse = models.CharField(max_length=255, default='ras')
    avatar = models.FileField(upload_to='avatars/', blank=True, null=True)
    status = models.CharField(max_length=255, blank=False, default="user")
    experience = models.CharField(max_length=255, blank=False,  default=0)

    def __str__(self):
        return "{0}".format(self.username)


class Pharmacie(BaseModel):
    libelle = models.CharField(max_length=10, default='')
    nom = models.CharField(null=False, max_length=255, default='')
    localisation = models.CharField(null=False, max_length=255, default='')
    tel = models.CharField(null=False, max_length=255, default='')
    email = models.EmailField(null=True, blank=True, default="patrick1kenne@gmail.com")
    latitude = models.FloatField(null=False, default=0)
    longitude = models.FloatField(null=False, default=0)
    h_ouverture = models.CharField(null=True, default="08:00 AM", max_length=15)
    h_fermeture = models.CharField(null=True, default="08:00 PM", max_length=15)
    user = models.ForeignKey(Utilisateur, related_name="pharmacies", on_delete=models.CASCADE, null=False, blank=False)

    
    
    def __str__(self):
        return "{0}".format(self.nom)  

    class Meta:
        ordering = ('-created_at',)

    def stocks(self, nom):
        return Medicament.objects.get(Q(nom=nom) & Q(pharmacie__id=self.id))


class Symptome(BaseModel):
    libelle = models.CharField(max_length=50)

    class Meta:
       ordering = ("-created_at",)

    def __str__(self):
        return "{0}".format(self.libelle)    


class Medicament(BaseModel):

    choices = (
        (0, 'bucale'),
        (1, 'injection'),
        (2, 'anale'),
    )
    nom = models.CharField(max_length=255, null=False, default="")
    prix = models.IntegerField(null=False, blank=False, default=1)
    # prixAchat = models.IntegerField(null=False, blank=False, default=1)
    marque = models.CharField(max_length=255, null=True, blank=True, default="Denk")
    date_exp = models.DateTimeField(null=True, blank=True, default="2042-06-10T17:07:03.121812Z")
    image = models.FileField(upload_to=upload_path, blank=True, null=True)
    masse = models.CharField(max_length=10, null=False, default="")
    qte_stock = models.PositiveBigIntegerField(null=False, blank=False, default=1)
    stockAlert = models.IntegerField(null=False, blank=False, default=1)
    stockOptimal = models.IntegerField(null=False, blank=False, default=1)
    description = models.TextField(default="")
    posologie = models.TextField(default="")
    voix = models.IntegerField(default=0, choices=choices)
    categorie = models.ForeignKey(Categorie, related_name="medicaments", on_delete=models.CASCADE)
    user = models.ForeignKey(Utilisateur, related_name="medicaments", on_delete=models.CASCADE, null=False, blank=False)
    pharmacie = models.ForeignKey(Pharmacie, related_name="medicaments", on_delete=models.CASCADE, null=True, blank=True)
    entrepot = models.ForeignKey('Entrepot', related_name="medicaments", on_delete=models.CASCADE, null=False, blank=False)


    class Meta:
        ordering = ('-created_at',)
        unique_together = ('nom', 'pharmacie',)

    def __str__(self):
        return "{0}".format(self.nom)

    def get_image_url(self):

        if self.image:
            return BASE_URL + self.image.url
        return BASE_URL + "/media/images/medecine_for.png"

    def pharmacies(self):
        medicaments = Medicament.objects.filter(Q(nom=self.nom))
        ids = [medicament.pharmacie_id for medicament in medicaments]
        pharmas = Pharmacie.objects.filter(id__in=ids)
        liste = [{
            "id": p.id,
            "nom": p.nom,
            "localisation": p.localisation,
            "tel": p.tel,
            "email": p.email,
            "stock": Medicament.objects.filter(
                Q(nom=self.nom) &  \
                Q(pharmacie=p.id)
            ).aggregate(stock=Sum('qte_stock'))['stock'],
            "latitude": p.latitude,
            "longitude": p.longitude,
            "h_ouverture": str(p.h_ouverture),
            "h_fermeture": str(p.h_fermeture),
            "user": p.user_id,
            "created_at": str(p.created_at),
            "updated_at": str(p.updated_at)
                }
                for p in pharmas
            ]
        return liste

    def get_pharmacie_name(self):
        return Pharmacie.objects.get(id=self.pharmacie_id).nom

    def entrepots(self):
        return Entrepot.objects.filter(Q(id=self.entrepot_id))

    def proprietaire(self):
        return Utilisateur.objects.get(id=self.user_id)

    def references(self):
        lignes = MedicamentFacture.objects.filter(medicament_id=self.id)
        ids = [ligne.facture_id for ligne in lignes]
        return Facture.objects.filter(id__in=ids)

    def historiques(self):
        return HistoriquePrix.objects.filter(medicament_id=self.id)


class Maladie(BaseModel):
    libelle = models.CharField(max_length=255, null=False)
    
    
    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return "{0}".format(self.libelle)        
        

class Consultation(BaseModel):
    symptome = models.ForeignKey(Symptome, on_delete=models.CASCADE)
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    maladie = models.ManyToManyField(Maladie, through="Carnet", blank=False)
   
    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return "{0}".format(self.symptome)

 
class Carnet(BaseModel):
    maladie = models.ForeignKey(Maladie, on_delete=models.CASCADE) 
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    user = models.IntegerField(blank=False, null=False, default=1)
    
    
    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return "{0}".format(self.maladie)


class Facture(BaseModel):
    utilisateur = models.ForeignKey(Utilisateur, related_name='factures', on_delete=models.CASCADE)
    medicaments = models.ManyToManyField(Medicament, through='MedicamentFacture')
    montantTotal = models.IntegerField(null=False, blank=False, default=1)
    quantiteTotal = models.IntegerField(null=False, blank=False, default=1)
    reduction = models.IntegerField(null=True, blank=True, default=0)
    note = models.TextField()
    # dateEcheance = models.DateTimeField()
    

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return "{0}".format(self.note)

    def produits(self):
        return MedicamentFacture.objects.filter(facture_id=self.id)

    def get_user_name(self):
        return Utilisateur.objects.get(pk=self.utilisateur_id).username


class MedicamentFacture(BaseModel):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
    medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE)
    montant = models.IntegerField(null=False, blank=False, default=1)
    quantite = models.IntegerField(null=False, blank=False, default=1)
    

    def montantTotal(self):
        return self.montant * self.quantite

    def get_medecine_name(self):
        return Medicament.objects.get(pk=self.medicament_id).nom

    class Meta:
        ordering = ('-created_at',)


class Entrepot(BaseModel):
    nom = models.CharField(max_length=255, default='')
    pays = models.CharField(max_length=255, default='')
    ville = models.CharField(max_length=255, default='')
    telephone = models.CharField(max_length=255, default='')
    description = models.TextField(default="")
    pharmacie = models.ForeignKey(Pharmacie, related_name="entrepots", on_delete=models.CASCADE)
    # medicaments = models.ManyToManyField(Medicament, through='EntrepotMedicament')
    

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return "{0}".format(self.nom)

    def valeurVente(self):
        medicaments = Medicament.objects.filter(entrepot_id=self.id)
        somme = 0
        for medoc in medicaments:
            somme += medoc.qte_stock * medoc.prix

        return somme

"""
class EntrepotMedicament(BaseModel):
    '''
        Cette classe liste les entrepôts d'un médicament donné
    '''
    entrepot = models.ForeignKey(Entrepot, on_delete=models.CASCADE)
    medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE)
    quantite = models.IntegerField(null=False, blank=False, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
"""


class Inventaire(BaseModel):
    libelle = models.TextField(default="")
    entrepot = models.ForeignKey(Entrepot, related_name="inventaires", on_delete=models.CASCADE)
    medicaments = models.ManyToManyField(Medicament, through='InventaireMedicament')
   

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return "{0}".format(self.libelle)

    def produits(self):
        return InventaireMedicament.objects.filter(inventaire_id=self.id)

    def get_entrepot_name(self):
        return Entrepot.objects.get(pk=self.entrepot_id).nom


class InventaireMedicament(BaseModel):
    inventaire = models.ForeignKey(Inventaire, on_delete=models.CASCADE)
    medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE)
    quantiteAttendue = models.IntegerField(null=False, blank=False, default=1)
    quantiteReelle = models.IntegerField(null=False, blank=False, default=1)
    
    def get_medecine_name(self):
        return Medicament.objects.get(pk=self.medicament_id).nom


class MouvementStock(BaseModel):
    entrepot = models.ForeignKey(Entrepot, on_delete=models.CASCADE)
    medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE, default=1)
    description = models.TextField(default="")
    quantite = models.IntegerField(null=False, blank=False, default=1)
    
    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.description

    def get_medecine_name(self):
        return Medicament.objects.get(pk=self.medicament_id).nom

    def get_entrepot_name(self):
        return Entrepot.objects.get(pk=self.entrepot_id).nom


class MouvementInventaire(BaseModel):
    pass


class HistoriquePrix(BaseModel):
    basePrix = models.CharField(max_length=255, default="HT")
    tva = models.FloatField(default=19.25)
    prixVente = models.IntegerField(null=False, blank=False, default=0) # Le prix de vente ici est en HT
    medicament = models.ForeignKey(Medicament, related_name="historiques", on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    

    class Meta:
        ordering = ('-created_at', )
