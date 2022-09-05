 

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
            'email',
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
            'get_pharmacie_name',
            'masse',
            'qte_stock',
            'stockAlert',
            'stockOptimal',
            'description',
            'posologie',
            'categorie',
            'user',
            'voix',
            'pharmacie',
            'entrepot',
            'created_at',
            'updated_at'
        ]


class EntrepotSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Entrepot

        fields = [
            'id',
            'nom',
            'pays',
            'ville',
            'telephone',
            'description',
            'pharmacie',
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
            'get_medecine_name',
            'montant',
            'quantite',
            'montantTotal',
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
    produits = MedicamentFactureSerializers(many=True, read_only=True)

    class Meta:
        model = models.Facture
        fields = [
            'id',
            'utilisateur',
            'get_user_name',
            #'medicaments',
            'montantTotal',
            'quantiteTotal',
            'reduction',
            'note',
            'created_at',
            'updated_at',
            'produits'
        ]


class EntrepotSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.Entrepot

        fields = [
            'id',
            'nom',
            'pays',
            'ville',
            'telephone',
            'description',
            'pharmacie',
            'created_at',
            'updated_at'
        ]


class EntrepotDetailsSerializers(serializers.ModelSerializer):
    medicaments = MedicamentSerialisers(many=True, read_only=True)

    class Meta:
        model = models.Entrepot

        fields = [
            'id',
            'nom',
            'pays',
            'ville',
            'telephone',
            'description',
            'pharmacie',
            'created_at',
            'updated_at',
            'medicaments'
        ]


class InventaireMedicamentSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.InventaireMedicament

        fields = [
            'id',
            'inventaire',
            'medicament',
            'get_medecine_name',
            'quantiteAttendue',
            'quantiteReelle',
            'created_at',
            'updated_at'
        ]


class InventaireSerializers(serializers.ModelSerializer):
    produits = InventaireMedicamentSerializers(many=True, read_only=True)

    class Meta:
        model = models.Inventaire

        fields = [
            'id', 
            'libelle',
            'entrepot',
            # 'medicaments',
            'get_entrepot_name',
            'created_at',
            'updated_at',
            'produits'
        ]


class MouvementStockSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.MouvementStock
        fields = [
            'id',
            'entrepot',
            'description',
            'quantite',
            'created_at',
            'updated_at'
        ]


class HistoriquePrixSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.HistoriquePrix
        fields = [
            'id',
            'basePrix',
            'tva',
            'prixVente',
            'medicament',
            'utilisateur',
            'created_at',
            'updated_at'
        ]


class MedicamentDetailSerialisers(serializers.ModelSerializer):
    entrepots = EntrepotSerializers(many=True, read_only=True)
    proprietaire = UtilisateurSerializer(many=False, read_only=True)
    references = FactureSerializers(many=True, read_only=True)
    historiques = HistoriquePrixSerializers(many=True, read_only=True)

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
            'created_at',
            'updated_at',
            'proprietaire',
            'entrepots',
            'references',
            'historiques'
        ]
