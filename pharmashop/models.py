from django.db import models
from django.contrib.auth.models import User



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


Base_URL = 'http://127.0.0.1:8000'


class Categorie(models.Model):
    libelle = models.CharField(max_length=50)
       
    def __str__(self):
        return "{0}".format(self.libelle) 


class Utilisateur(User):
    adresse = models.CharField(max_length=255)
    avatar = models.FileField(upload_to='avatar/', blank=True, null=True)
    status = models.CharField(max_length=255, blank=False, default="user")
    experience = models.CharField(max_length=255,blank=False,  default=0)


    def __str__(self):
        return "{0}".format(self.username)    

class Symptome(models.Model):
    libelle= models.CharField(max_length=50)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    class Meta:
       ordering=("-created_at",) 

    def __str__(self):
        return "{0}".format(self.libelle)    


class Pharmacie(models.Model):
    nom = models.CharField(null=False, max_length=255)
    localisation = models.CharField(null=False, max_length=255)
    tel = models.CharField(null=False, max_length=255)
    latitude = models.FloatField(null=False,default=0)
    longitude = models.FloatField(null=False, default=0)
    h_ouverture = models.DateTimeField(null=True)
    h_fermeture = models.DateTimeField(null=True)
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, null=False, blank=False)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    class Meta:        
        ordering=('-created_at',)
    
    def __str__(self):
        return "{0}".format(self.nom)  


class Medicament(models.Model):

    nom = models.CharField(max_length=255, null=False)
    prix = models.DecimalField(null=False, blank=False, decimal_places=5, max_digits=10)
    marque = models.CharField(max_length=255, null=False)
    date_exp = models.DateTimeField(null=False,)
    image = models.FileField(upload_to='images/', blank=False, null= False)
    masse = models.CharField(max_length=10, null=False)
    qte_stock = models.IntegerField(null=False, blank=False)
    description = models.CharField(max_length=255)
    posologie = models.CharField(max_length=255)
    categorie=models.ForeignKey(Categorie, related_name="medicaments", on_delete=models.CASCADE)
    user = models.ForeignKey(Utilisateur, related_name= "medicaments", on_delete=models.CASCADE, null=True, blank=True)
    pharmacie = models.ForeignKey(Pharmacie, on_delete=models.CASCADE, null=False, blank=False)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)

    class Meta:
        ordering=('-created_at',)

    def __str__(self):
        return "{0}".format(self.nom)

class Maladie(models.Model):
    libelle = models.CharField(max_length=255, null=False)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)        
    
    class Meta:
        ordering=('-created_at',)

    def __str__(self):
        return "{0}".format(self.libelle)        
        

class Consultaion(models.Model):
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
    consultation = models.ForeignKey(Consultaion, on_delete=models.CASCADE)
    user = models.IntegerField(blank=False, null=False, default=1)
    created_at =models.DateTimeField(auto_now_add=True)
    updated_at =models.DateTimeField(auto_now=True)        
    
    class Meta:
        ordering=('-created_at',)

    def __str__(self):
        return "{0}".format(self.maladie)




            


