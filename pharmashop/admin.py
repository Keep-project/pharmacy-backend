from django.contrib import admin

from pharmashop import models

# Register your models here.

admin.site.register([
    models.Categorie,
    models.Utilisateur,
    models.Pharmacie,
    models.Symptome,
    models.Medicament,
    models.Maladie,
    models.Consultation,
    models.Carnet,
    models.Facture,
    models.MedicamentFacture,
    models.Entrepot,
    models.Inventaire,
    models.InventaireMedicament,
    models.MouvementStock,
    models.MouvementInventaire,
    models.HistoriquePrix,
])
