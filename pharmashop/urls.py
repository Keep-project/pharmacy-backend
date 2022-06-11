

from django.urls import path, re_path
from pharmashop import views 
urlpatterns = [

                    #gestion des Pharmacies
    path("pharmacie", views.PharmacieViewSet.as_view({'get': 'list', 'post': 'post'})),
    re_path("pharmacie/(?P<id>\d+)$", views.PharmacieDetailViewSet.as_view({'get': 'retrieve', 'put':'put', 'delete':'delete'})),

                    #gestion des categories
    path("categorie", views.CategorieViewSet.as_view({'get': 'list','post':'post'})),
   re_path("categorie/(?P<id>\d+)$", views.CategorieDetailViewSet.as_view({'get': 'retrieve', 'put':'put', 'delete':'delete'})),

                        #gestion des categories
    path("utilisateur", views.UtilisateurViewSet.as_view({'get': 'list', 'post':'post'})),
    re_path("utilisateur/(?P<id>\d+)$", views.UtilisateurDetailViewSet.as_view({'get': 'retrieve', 'put':'put', 'delete':'delete'})),

      #gestion des categories
    path("medicament", views.MedicamentViewSet.as_view({'get': 'list',})),
    re_path("medicament/(?P<id>\d+)$", views.MedicamentDetailViewSet.as_view({'get': 'retrieve', 'put':'put', 'delete':'delete'})),

    
]
