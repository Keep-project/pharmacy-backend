

from django.urls import path, re_path
from pharmashop import views 
urlpatterns = [

    #gestion des Pharmacies
    re_path(r"^pharmacie/$", views.PharmacieViewSet.as_view({'get': 'list', 'post': 'post'})),
    re_path(r"^pharmacie/(?P<id>\d+)$", views.PharmacieDetailViewSet.as_view({'get': 'retrieve', 'put':'put', 'delete':'delete'})),
    re_path(r"^pharmacie/me$", views.ListPhamacieForUser.as_view({'get': 'list', })),

    #gestion des categories
    path("categorie/", views.CategorieViewSet.as_view({'get': 'list','post':'post'})),
    re_path(r"^categorie/(?P<id>\d+)$", views.CategorieDetailViewSet.as_view({'get': 'retrieve', 'put':'put', 'delete':'delete'})),
    

    #gestion des categories
    re_path(r"^utilisateur/$", views.UtilisateurViewSet.as_view({'get': 'list', 'post':'post'})),
    # path("jwt/create", views.UtilisateurViewSet.as_view({'get': 'list', 'post':'post'})),
    re_path(r"^utilisateur/(?P<id>\d+)$", views.UtilisateurDetailViewSet.as_view({'get': 'retrieve', 'put':'put', 'delete':'delete'})),

    #gestion des medicaments
    path("medicament", views.MedicamentViewSet.as_view({'get': 'list',})),
    re_path(r"^medicament/(?P<id>\d+)$", views.MedicamentDetailViewSet.as_view({'get': 'retrieve', 'put':'put', 'delete':'delete'})),
    re_path(r"^medicament/me/(?P<idPharmacie>\d+)$", views.ListMedicamentForPhamacie.as_view({'get': 'list', })),
    re_path(r"^categorie/me/(?P<idCategorie>\d+)$", views.ListCategorieForMedicament.as_view({'get': 'list', })),

    #gestion des Symptomes
    path("symptome/", views.SymptomeViewSet.as_view({'get': 'list','post':'post'})),
    re_path(r"^symptome/(?P<id>\d+)$", views.SymptomeDetailViewSet.as_view({'get': 'retrieve', 'put':'put', 'delete':'delete'})),

    #gestion des consultations
    path("consultation/", views.ConsultationViewSet.as_view({'get': 'list','post':'post'})),
    re_path(r"^consultation/(?P<id>\d+)$", views.ConsultationDetailViewSet.as_view({'get': 'retrieve', 'put':'put', 'delete':'delete'})),
    re_path(r"^consultation/me$", views.ListconsultationForUser.as_view({'get': 'list', })),


    # gestion des maladies
    path("maladie/", views.MaladieViewSet.as_view({'get': 'list','post':'post'})),
    re_path(r"^maladie/(?P<id>\d+)$", views.MaladieDetailViewSet.as_view({'get': 'retrieve', 'put':'put', 'delete':'delete'})),

     # gestion des carnets
    path("carnet/", views.CarnetViewSet.as_view({'get': 'list','post':'post'})),
    re_path(r"^carnet/(?P<id>\d+)$", views.CaranetDetailViewSet.as_view({'get': 'retrieve', 'put':'put', 'delete':'delete'})),

    
]
                      