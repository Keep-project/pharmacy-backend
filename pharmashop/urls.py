

from django.urls import path, re_path
from pharmashop import views

urlpatterns = [

    # gestion des Pharmacies
    re_path(r"^pharmacie/$", views.PharmacieViewSet.as_view({'get': 'list', 'post': 'post'})),
    re_path(r"^pharmacie/(?P<id>\d+)$", views.PharmacieDetailViewSet.as_view({'get': 'retrieve', 'put': 'put','delete': 'delete'})),
    re_path(r"^pharmacie/me$", views.ListPhamacieForUser.as_view({'get': 'list', })),

    # gestion des categories
    path("categorie/", views.CategorieViewSet.as_view({'get': 'list','post':'post'})),
    re_path(r"^categorie/(?P<id>\d+)$", views.CategorieDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete': 'delete'})),
    

    # gestion des categories
    re_path(r"^utilisateur/$", views.UtilisateurViewSet.as_view({'get': 'list', 'post': 'post'})),
    # path("jwt/create", views.UtilisateurViewSet.as_view({'get': 'list', 'post':'post'})),
    re_path(r"^utilisateur/(?P<id>\d+)$", views.UtilisateurDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete': 'delete'})),

    #  des medicaments
    re_path(r"^medicament/$", views.MedicamentViewSet.as_view({'get': 'list', })),
    re_path(r"^medicament/(?P<id>\d+)$", views.MedicamentDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete': 'delete'})),
    re_path(r"^medicamentDetail/(?P<id>\d+)$", views.DetailMedicamentViewset.as_view({'get': 'retrieve', })),
    re_path(r"^medicament/me/(?P<id>\d+)$", views.ListMedicamentForPhamacie.as_view({'get': 'list', })),
    re_path(r'^filter/$', views.FilterMedicamentViewSet.as_view({'get': 'list', }), ),
    re_path(r"^categories/me/(?P<id>\d+)$", views.ListCategorieForMedicament.as_view({'get': 'list', })),

    # gestion des Symptomes
    path("symptome/", views.SymptomeViewSet.as_view({'get': 'list', 'post': 'post'})),
    re_path(r"^symptome/(?P<id>\d+)$", views.SymptomeDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete': 'delete'})),

    # gestion des consultations
    path("consultation/", views.ConsultationViewSet.as_view({'get': 'list', 'post': 'post'})),
    re_path(r"^consultation/(?P<id>\d+)$", views.ConsultationDetailViewSet.as_view({'get': 'retrieve', 'put':'put', 'delete': 'delete'})),
    re_path(r"^consultation/me$", views.ListconsultationForUser.as_view({'get': 'list', })),


    # gestion des maladies
    path("maladie/", views.MaladieViewSet.as_view({'get': 'list','post':'post'})),
    re_path(r"^maladie/(?P<id>\d+)$", views.MaladieDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete': 'delete'})),

    # gestion des carnets
    path("carnet/", views.CarnetViewSet.as_view({'get': 'list','post':'post'})),
    re_path(r"^carnet/(?P<id>\d+)$", views.CarnetDetailViewSet.as_view({'get': 'retrieve', 'put':'put', 'delete': 'delete'})),


    # Générer des pdfs
    re_path(r'^utilisateurs/pdf/$', views.DownloadPDF.as_view({"get": "get"}), name="users_pdf"),

    # Gestion de la facturation
    re_path(r"^facture/$", views.FactureViewSet.as_view({'get': 'list', 'post':'post'}), name='liste_facture'),
    re_path(r"^facture/(?P<id>\d+)$", views.FactureDetailViewSet.as_view({'get': 'retrieve', 'put':'put', 'delete': 'delete'}), name='detail_facture'),

    # Gestion des entrepôts
    re_path(r"^entrepot/$", views.EntrepotViewSet.as_view({'get': 'list', 'post':'post'}), name='liste_entrepot'),
    re_path(r"^entrepot/(?P<id>\d+)$", views.EntrepotDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete':'delete'}), name='detail_entrepot'),


    # Gestion des inventaires
    re_path(r"^inventaire/$", views.InventaireViewSet.as_view({'get': 'list', 'post':'post'}), name='liste_entrepot'),
    re_path(r"^inventaire/(?P<id>\d+)$", views.InventaireDetailViewSet.as_view({'get': 'retrieve', 'put': 'put', 'delete':'delete'}), name='detail_entrepot'),


    # Gestion des mouvements de stock
    re_path(r"^mouvement/$", views.MouvementStockViewSet.as_view({'get': 'list', 'post': 'post'}), name='liste_entrepot'),
    re_path(r"^mouvement/(?P<id>\d+)$", views.MouvementStockDetailViewSet.as_view({'get': 'retrieve', 'put':'put', 'delete': 'delete'}), name='detail_entrepot'),

]
                      