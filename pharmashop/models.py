from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q



# Create your models here.
# liste des models
#  -pharmacie
#  -medicament
#  -catégorie
#  -utilisateur
#  -maladie
#  -symptôme
#  -consultation
#  -carnet (portant les informations de la consultation)


BASE_URL = 'http://192.168.220.1:8000'


class Categorie(models.Model):
    libelle = models.CharField(max_length=50)
       
    def __str__(self):
        return "{0}".format(self.libelle)
        

class Utilisateur(User):
    adresse = models.CharField(max_length=255, default='ras')
    avatar = models.FileField(upload_to='avatars/', blank=True, null=True)
    status = models.CharField(max_length=255, blank=False, default="user")
    experience = models.CharField(max_length=255,blank=False,  default=0)

    def __str__(self):
        return "{0}".format(self.username) 


class Pharmacie(models.Model):
    libelle = models.CharField(max_length=10, default='')
    nom = models.CharField(null=False, max_length=255, default='')
    localisation = models.CharField(null=False, max_length=255, default='')
    tel = models.CharField(null=False, max_length=255, default='')
    latitude = models.FloatField(null=False,default=0)
    longitude = models.FloatField(null=False, default=0)
    h_ouverture = models.DateTimeField(null=True,)
    h_fermeture = models.DateTimeField(null=True)
    user = models.ForeignKey(Utilisateur, related_name="pharmacies",on_delete=models.CASCADE, null=False, blank=False)

    created_at =models.DateTimeField(auto_now_add=True,)
    updated_at =models.DateTimeField(auto_now=True,)
    
    def __str__(self):
        return "{0}".format(self.nom)  

    class Meta:
        ordering=('-created_at',)

       

class Symptome(models.Model):
    libelle= models.CharField(max_length=50)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    class Meta:
       ordering=("-created_at",) 

    def __str__(self):
        return "{0}".format(self.libelle)    



class Medicament(models.Model):

    choices = (
        (0, 'bucale'),
        (1, 'injection'),
        (2, 'anale')
    )
    nom = models.CharField(max_length=255, null=False)
    prix = models.IntegerField(null=False, blank=False, default=1)
    marque = models.CharField(max_length=255, null=False)
    date_exp = models.DateTimeField(null=False,)
    image = models.FileField(upload_to='images/', blank=False, null= False)
    masse = models.CharField(max_length=10, null=False)
    qte_stock = models.IntegerField(null=False, blank=False, default=1)
    stockAlert = models.IntegerField(null=False, blank=False, default=1)
    stockOptimal = models.IntegerField(null=False, blank=False, default=1)
    description = models.TextField()
    posologie = models.TextField()
    voix = models.IntegerField(default=0, choices=choices )
    categorie= models.ForeignKey(Categorie, related_name="medicaments", on_delete=models.CASCADE)
    user = models.ForeignKey(Utilisateur, related_name= "medicaments", on_delete=models.CASCADE, null=True, blank=True)
    pharmacie = models.ForeignKey(Pharmacie, related_name="medicaments", on_delete=models.CASCADE, null=True, blank=True)
    entrepot = models.ForeignKey('Entrepot', related_name="medicaments", on_delete=models.CASCADE, null=True, blank=True)

    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('-created_at',)

    def __str__(self):
        return "{0}".format(self.nom)

    def get_image_url(self):

        if self.image:
            return BASE_URL + self.image.url
        return BASE_URL + "/media/images/default-image.jpg"

    def pharmacies(self):
        medicaments = Medicament.objects.filter(Q(nom__icontains=self.nom))
        ids = [ medicament.pharmacie_id for medicament in medicaments ] 
        return Pharmacie.objects.filter(id__in=ids)


class Maladie(models.Model):
    libelle = models.CharField(max_length=255, null=False)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)        
    
    class Meta:
        ordering=('-created_at',)

    def __str__(self):
        return "{0}".format(self.libelle)        
        

class Consultation(models.Model):
    symptome = models.ForeignKey(Symptome, on_delete=models.CASCADE)
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    maladie = models.ManyToManyField(Maladie, through="Carnet", blank=False)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('-created_at',)


    def __str__(self):
        return "{0}".format(self.symptome)

 
class Carnet(models.Model):
    maladie = models.ForeignKey(Maladie, on_delete=models.CASCADE) 
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    user = models.IntegerField(blank=False, null=False, default=1)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)        
    
    class Meta:
        ordering=('-created_at',)

    def __str__(self):
        return "{0}".format(self.maladie)


class Facture(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, related_name='factures', on_delete=models.CASCADE)
    medicament = models.ManyToManyField(Medicament, through='MedicamentFacture')
    montantTotal = models.IntegerField(null=False, blank=False, default=1)
    quantiteTotal = models.IntegerField(null=False, blank=False, default=1)
    reduction = models.IntegerField(null=False, blank=False, default=0)
    note = models.TextField()
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('-created_at',)

    def __str__(self):
        return "{0}".format(self.note)


class MedicamentFacture(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE)
    medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE)
    montant = models.IntegerField(null=False, blank=False, default=1)
    quantite = models.IntegerField(null=False, blank=False, default=1)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)



class Entrepot(models.Model):
    nom = models.CharField(max_length=255)
    pays = models.CharField(max_length=255)
    ville = models.CharField(max_length=255)
    telephone = models.CharField(max_length=255)
    description = models.TextField()
    pharmacie = models.ForeignKey(Pharmacie, related_name="entrepots", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('-created_at',)

    def __str__(self):
        return "{0}".format(self.nom)


class Inventaire(models.Model):
    libelle = models.TextField()
    entrepot = models.ForeignKey(Entrepot, related_name="inventaires", on_delete=models.CASCADE)
    medicament = models.ManyToManyField(Medicament, through='InventaireMedicament')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('-created_at',)

    def __str__(self):
        return "{0}".format(self.libelle)


class InventaireMedicament(models.Model):
    inventaire = models.ForeignKey(Inventaire, on_delete=models.CASCADE)
    medicament = models.ForeignKey(Medicament, on_delete=models.CASCADE)
    quantiteAttendue = models.IntegerField(null=False, blank=False, default=1)
    quantiteReelle = models.IntegerField(null=False, blank=False, default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

