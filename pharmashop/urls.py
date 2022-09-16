

from django.urls import path, re_path
from . import views

urlpatterns = [

    # Controle de permission des utilisateurs
    re_path(r"^permission/(?P<codename>\w+)$", views.HasPermissionViewSet.as_view({'get': 'list'})),

    # gestion des Pharmacies
    re_path(r"^pharmacie/$", views.PharmacieViewSet.as_view({'get': 'list', 'post': 'post'})),
    re_path(r"^pharmacie/(?P<id>\d+)$",  \
            views.PharmacieDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete': 'delete'})),
    re_path(r"^pharmacie/me/$", views.ListPhamacieForUser.as_view({'get': 'list', })),

    # Liste des pharmacies proches
    re_path(r'^pharmacie/proche/(?P<d>\d+)$', views.PharmacieProcheViewSet.as_view({'get': 'list', 'post': 'list'})),
    re_path(r'^pharmacie/filter/$', views.PharmacieFilterViewSet.as_view({'post': 'list'})),

    # gestion des categories
    path("categorie/", views.CategorieViewSet.as_view({'get': 'list', 'post': 'post'})),
    re_path(r"^categorie/(?P<id>\d+)$",  \
            views.CategorieDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete': 'delete'})),
    

    # gestion des categories
    re_path(r"^utilisateur/$", views.UtilisateurViewSet.as_view({'get': 'list', 'post': 'post'})),
    # path("jwt/create", views.UtilisateurViewSet.as_view({'get': 'list', 'post':'post'})),
    re_path(r"^utilisateur/(?P<id>\d+)$", \
            views.UtilisateurDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete': 'delete'})),

    #  des medicaments
    re_path(r"^medicament/$", views.MedicamentViewSet.as_view({'get': 'list', })),
    re_path(r"^medicament/(?P<id>\d+)$",  \
            views.MedicamentDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete': 'delete'})),
    re_path(r"^medicamentDetail/(?P<id>\d+)$", views.DetailMedicamentViewset.as_view({'get': 'retrieve', })),
    re_path(r"^medicament/me/(?P<id>\d+)$", views.ListMedicamentForPhamacie.as_view({'post': 'list'})),
    re_path(r'^medicament/filter/$', views.FilterMedicamentViewSet.as_view({'post': 'list', }), ),
    re_path(r"^categories/me/(?P<id>\d+)$", views.ListCategorieForMedicament.as_view({'get': 'list', })),

    # gestion des Symptomes
    path("symptome/", views.SymptomeViewSet.as_view({'get': 'list', 'post': 'post'})),
    re_path(r"^symptome/(?P<id>\d+)$",  \
            views.SymptomeDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete': 'delete'})),

    # gestion des consultations
    path("consultation/", views.ConsultationViewSet.as_view({'get': 'list', 'post': 'post'})),
    re_path(r"^consultation/(?P<id>\d+)$",  \
            views.ConsultationDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete': 'delete'})),
    re_path(r"^consultation/me$", views.ListconsultationForUser.as_view({'get': 'list', })),

    # gestion des maladies
    path("maladie/", views.MaladieViewSet.as_view({'get': 'list', 'post': 'post'})),
    re_path(r"^maladie/(?P<id>\d+)$",  \
            views.MaladieDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete': 'delete'})),

    # gestion des carnets
    path("carnet/", views.CarnetViewSet.as_view({'get': 'list', 'post': 'post'})),
    re_path(r"^carnet/(?P<id>\d+)$",  \
            views.CarnetDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete': 'delete'})),


    # Générer des pdfs
    re_path(r'^utilisateurs/pdf/$', views.DownloadPDF.as_view({"get": "get"}), name="users_pdf"),
    re_path(r'^utilisateurs/pdfs/$', views.GeneratePDF.as_view({"get": "get"}), name="users_pdfs"),

    # Gestion de la facturation
    re_path(r"^facture/$", views.FactureViewSet.as_view({'get': 'list', 'post': 'post'}), name='liste_facture'),
    re_path(r"^facture/(?P<id>\d+)$",  \
            views.FactureDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete': 'delete'}),  \
            name='detail_facture'),
    re_path(r"^facture/me/(?P<idPharmacy>\d+)$", views.FactureForPharmacyViewSet.as_view({'get': 'list', 'post': 'list'}), \
            name='liste_facture_pharmacie'),

    # Gestion des entrepôts
    re_path(r"^entrepot/$", views.EntrepotViewSet.as_view({'post': 'post'}), name='poster_entrepot'),
    re_path(r"^entrepot/(?P<id>\d+)$",  \
            views.EntrepotDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete': 'delete'}),  \
            name='detail_entrepot'),

    re_path(r"^entrepot/pharmacy/(?P<idPharmacy>\d+)$", views.EntrepotForPharmacyViewSet.as_view({'get': 'list', \
            'post': 'list'}), name='poster_entrepot'),

    re_path(r"^entrepot/pharmacy/(?P<idPharmacy>\d+)/list$", views.EntrepotForPharmacyListViewSet.as_view({'get': 'list', \
            'post': 'list'}), name='poster_entrepot_list'),

    re_path(r"^entrepot/medecine/(?P<idEntrepot>\d+)/list$", views.MedicamentForEntrepotViewSet.as_view({'get': 'list', \
            'post': 'list'}), name='poster_entrepot_list_medecine'),


    # Gestion des inventaires
    re_path(r"^inventaire/$", views.InventaireViewSet.as_view({'get': 'list', 'post': 'post'}),  \
            name='liste_entrepot'),
    re_path(r"^inventaire/(?P<id>\d+)$", \
            views.InventaireDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete': 'delete'}),  \
            name='detail_entrepot'),
    re_path(r"^inventaire/me/(?P<idPharmacy>\d+)$", views.InventaireForPharmacyViewSet.as_view({'get': 'list', 'post': 'list'}), \
            name='liste_inventaire_pharmacie'),


    # Gestion des mouvements de stock
    re_path(r"^mouvement/$", views.MouvementStockViewSet.as_view({'get': 'list', 'post': 'post'}),  \
            name='liste_entrepot'),
    re_path(r"^mouvement/(?P<id>\d+)$",  \
            views.MouvementStockDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete': 'delete'}), \
            name='detail_entrepot'),

    re_path(r"^mouvement/pharmacy/(?P<idPharmacy>\d+)$", views.MouvementStockForPharmacyViewSet.as_view({'get': 'list', 'post': 'list'}), \
            name='liste_mouvement_pharmacie'),

    re_path(r"^mouvement/medecine/(?P<idMedecine>\d+)$", views.MouvementStockForMedecineViewSet.as_view({'get': 'list', 'post': 'list'}), \
            name='liste_mouvement_pharmacie'),

]
                      