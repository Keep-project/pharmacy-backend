 

from rest_framework import serializers
from  django.contrib.auth.models import User
from .models import Carnet, Maladie, Medicament, Symptome,Utilisateur,Categorie,Consultaion,Pharmacie


class CategorieSerializers(serializers.ModelSerializer):


    class Meta:
        model = Categorie
        fields = [
            'id',
            'libelle'
            
        ]

class UtilisateurSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Utilisateur
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
        model = Pharmacie
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
        model = Medicament
        fields = [
            'id',
            'nom',
            'prix',
            'marque',
            'date_exp',
            'image',
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

class SymptomeSerializers(serializers.ModelSerializer):


    class Meta:
        model = Symptome
        fields = [
            'id',
            'libelle'
        ]           

class ConsultationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Consultaion
        fields = [
            'id',
            'user',
            'symptome',
            'created_at',
            'updated_at'
        ]
        
class MaladieSerializers(serializers.ModelSerializer):
    class Meta:
        model = Maladie
        fields = [
            'id',
            'libelle',
            'created_at',
            'updated_at'
        ]        


class CarnetSerializers(serializers.ModelSerializer):
    class Meta:
        model = Carnet
        fields = [
            'id',
            'maladie',
            'consultation',
            'created_at',
            'updated_at'
        ]
        