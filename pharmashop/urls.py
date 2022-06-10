

from django.urls import path
from pharmashop import views 
urlpatterns = [

                    #gestion des Pharmacies
    path("pharmacie", views.PharmacieViewSet.as_view({'get': 'list', 'post': 'post'})),

                    #gestion des categories
    path("categorie", views.CategorieViewSet.as_view({'get': 'list','post':'post'})),

                        #gestion des categories
    path("utilisateur", views.UtilisateurViewSet.as_view({'get': 'list', 'post':'post'})),

    
]
