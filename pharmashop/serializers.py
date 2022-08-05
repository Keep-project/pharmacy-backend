 

from rest_framework import serializers
from  django.contrib.auth.models import User
from pharmashop import models


class CategorieSerializers(serializers.ModelSerializer):


    class Meta:
        model = models.Categorie
        fields = [
            'id',
            'libelle'
        ]

class CategorieTestSerializers(serializers.ModelSerializer):


    class Meta:
        model = models.Pharmacie
        fields = [
            'id',
            'nom'
        ]

class SymptomeSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Symptome
        fields = [
            'id',
            'libelle'
        ]

class UtilisateurSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Utilisateur
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'adresse',
            'email',
            'is_staff',
            'is_active',
            'last_login',
            'is_superuser',
            'date_joined',
            'user_permissions'
        ]   



class PharmacieSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Pharmacie
        fields = [
            'id',
            'nom',
            'localisation',
            'tel',
            'latitude',
            'longitude',
            'h_ouverture',
            'h_fermeture',
            'user',
            'created_at',
            'updated_at'
        ]        

class MedicamentSerialisers(serializers.ModelSerializer):
    class Meta:
        model = models.Medicament
        fields = [
            'id',
            'nom',
            'prix',
            'marque',
            'date_exp',
            'get_image_url',
            'masse',
            'qte_stock',
            'description',
            'posologie',
            'categorie',
            'user',
            'voix',
            'pharmacie',
            'created_at',
            'updated_at'
        ]  

class MedicamentDetailSerialisers(serializers.ModelSerializer):
    pharmacies = PharmacieSerializers(many=True, read_only=True)
    class Meta:
        model = models.Medicament
        fields = [
            'id',
            'nom',
            'prix',
            'marque',
            'date_exp',
            'get_image_url',
            'masse',
            'qte_stock',
            'stockAlert',
            'stockOptimal',
            'description',
            'posologie',
            'categorie',
            'user',
            'voix',
            'pharmacies',
            'created_at',
            'updated_at'
        ]  
           

class ConsultationSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Consultation
        fields = [
            'id',
            'user',
            'symptome',
            'created_at',
            'updated_at'
        ]
        
class MaladieSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Maladie
        fields = [
            'id',
            'libelle',
            'created_at',
            'updated_at'
        ]        


class CarnetSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Carnet
        fields = [
            'id',
            'maladie',
            'consultation',
            'created_at',
            'updated_at'
        ]



class FactureSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Facture
        fields = [
            'id',
            'utilisateur',
            'medicaments',
            'montantTotal',
            'quantiteTotal',
            'reduction',
            'note',
            'created_at',
            'updated_at'
        ]



class MedicamentFactureSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.MedicamentFacture

        fields = [
            'id',
            'facture',
            'medicament',
            'montant',
            'quantite',
            'created_at',
            'updated_at'
        ]



class EntrepotSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.Entrepot

        fields = [
            'nom',
            'pays',
            'ville',
            'telephone',
            'description',
            'pharmacie',
            'created_at',
            'updated_at'
        ]


class InventaireSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.Inventaire

        fields = [
            'id', 
            'libelle',
            'entrepot',
            'medicament',
            'created_at',
            'updated_at'
        ]



class InventaireMedicamentSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.InventaireMedicament

        fields = [
            'id',
            'inventaire',
            'medicament',
            'quantiteAttendue',
            'quantiteReelle',
            'created_at',
            'updated_at'
        ]