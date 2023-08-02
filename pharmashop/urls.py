

from django.urls import path, re_path
from . import views

urlpatterns = [

    # Creation du backup automatique

    # path('backup/', views.backup),
    # path('restore/', views.restore),
    # path('dumpdata/', views.dumpdata),
    # path('loadata/', views.loaddata),


    # Controle de permission des utilisateurs
    re_path(r"^permission/(?P<codename>\w+)$", views.HasPermissionViewSet.as_view({'get': 'list'})),

    # gestion des Pharmacies
    re_path(r"^pharmacie/$", views.PharmacieViewSet.as_view({'get': 'list', 'post': 'post'})),
    path("pharmacie/<str:id>",  \
            views.PharmacieDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete': 'delete'})),
    re_path(r"^pharmacie/me/$", views.ListPhamacieForUser.as_view({'get': 'list', })),

    # Liste des pharmacies proches
    path('pharmacie/proche/<int:rayon>', views.PharmacieProcheViewSet.as_view({'get': 'list', 'post': 'list'})),
    re_path(r'^pharmacie/filter/$', views.PharmacieFilterViewSet.as_view({'post': 'list'})),

    # gestion des categories
    path("categorie/", views.CategorieViewSet.as_view({'get': 'list', 'post': 'post'})),
    path("categorie/<str:id>/",  \
            views.CategorieDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete': 'delete'})),
    

    # gestion des categories
    re_path(r"^utilisateur/$", views.UtilisateurViewSet.as_view({'get': 'list', 'post': 'post'})),
    # path("jwt/create", views.UtilisateurViewSet.as_view({'get': 'list', 'post':'post'})),
    re_path(r"^utilisateur/(?P<id>\d+)$", \
            views.UtilisateurDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete': 'delete'})),

    #  des medicaments
    re_path(r"^medicament/$", views.MedicamentViewSet.as_view({'get': 'list', })),
    path("medicament/<str:id>",  \
            views.MedicamentDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete': 'delete'})),
    path("medicamentDetail/<str:id>", views.DetailMedicamentViewset.as_view({'get': 'retrieve', })),
    path("medicament/me/<str:id>", views.ListMedicamentForPhamacie.as_view({'post': 'list'})),
    re_path(r'^medicament/filter/$', views.FilterMedicamentViewSet.as_view({'post': 'list', }), ),
    path("categories/me/<str:id>", views.ListCategorieForMedicament.as_view({'get': 'list', })),

    # gestion des Symptomes
    path("symptome/", views.SymptomeViewSet.as_view({'get': 'list', 'post': 'post'})),
    path("symptome/<str:id>",  \
            views.SymptomeDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete': 'delete'})),

    # gestion des consultations
    path("consultation/", views.ConsultationViewSet.as_view({'get': 'list', 'post': 'post'})),
    path("consultation/<str:id>",  \
            views.ConsultationDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete': 'delete'})),
    re_path(r"^consultation/me$", views.ListconsultationForUser.as_view({'get': 'list', })),

    # gestion des maladies
    path("maladie/", views.MaladieViewSet.as_view({'get': 'list', 'post': 'post'})),
    path("maladie/<str:id>",  \
            views.MaladieDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete': 'delete'})),

    # gestion des carnets
    path("carnet/", views.CarnetViewSet.as_view({'get': 'list', 'post': 'post'})),
    re_path("carnet/<str:id>",  \
            views.CarnetDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete': 'delete'})),


    # Générer des pdfs
    re_path(r'^utilisateurs/pdf/$', views.DownloadPDF.as_view({"get": "get"}), name="users_pdf"),
    re_path(r'^utilisateurs/pdfs/$', views.GeneratePDF.as_view({"get": "get"}), name="users_pdfs"),

    re_path(r'^utilisateurs/setpassword/$', views.SetPasswordViewSet.as_view({"post": "post", "put": "post"}),
            name="set_password"),

    # Gestion de la facturation
    re_path(r"^facture/$", views.FactureViewSet.as_view({'get': 'list', 'post': 'post'}), name='liste_facture'),
    path("facture/<str:id>",  \
            views.FactureDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete': 'delete'}),  \
            name='detail_facture'),
    path("facture/me/<str:idPharmacy>", views.FactureForPharmacyViewSet.as_view({'get': 'list', 'post': 'list'}), \
            name='liste_facture_pharmacie'),

    # Gestion des entrepôts
    re_path(r"^entrepot/$", views.EntrepotViewSet.as_view({'post': 'post'}), name='poster_entrepot'),
    path("entrepot/<str:id>",  \
            views.EntrepotDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete': 'delete'}),  \
            name='detail_entrepot'),

    path("entrepot/pharmacy/<str:idPharmacy>", views.EntrepotForPharmacyViewSet.as_view({'get': 'list', \
            'post': 'list'}), name='poster_entrepot'),

    path("entrepot/pharmacy/<str:idPharmacy>/list", views.EntrepotForPharmacyListViewSet.as_view({'get': 'list', \
            'post': 'list'}), name='poster_entrepot_list'),

    path("entrepot/medecine/<str:idEntrepot>/list", views.MedicamentForEntrepotViewSet.as_view({'get': 'list', \
            'post': 'list'}), name='poster_entrepot_list_medecine'),


    # Gestion des inventaires
    re_path(r"^inventaire/$", views.InventaireViewSet.as_view({'get': 'list', 'post': 'post'}),  \
            name='liste_entrepot'),
    path("inventaire/<str:id>", \
            views.InventaireDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete': 'delete'}),  \
            name='detail_entrepot'),
    path("inventaire/me/<str:idPharmacy>", views.InventaireForPharmacyViewSet.as_view({'get': 'list', 'post': 'list'}), \
            name='liste_inventaire_pharmacie'),


    # Gestion des mouvements de stock
    re_path(r"^mouvement/$", views.MouvementStockViewSet.as_view({'get': 'list', 'post': 'post'}),  \
            name='liste_entrepot'),
    path("mouvement/<str:id>",  \
            views.MouvementStockDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete': 'delete'}), \
            name='detail_entrepot'),

    path("mouvement/pharmacy/<str:idPharmacy>", views.MouvementStockForPharmacyViewSet.as_view({'get': 'list', 'post': 'list'}), \
            name='liste_mouvement_pharmacie'),

    path("mouvement/medecine/<str:idMedecine>", views.MouvementStockForMedecineViewSet.as_view({'get': 'list', 'post': 'list'}), \
            name='liste_mouvement_pharmacie'),

]
                      