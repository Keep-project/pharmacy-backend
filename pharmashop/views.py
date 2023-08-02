import json

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from django.db import IntegrityError, transaction
import django

from . import models, serializers

from .helpers import distance, generateReport, hasPermission, addPermission, removePermission, clearPermissions, \
    base64_file, baseUrl, save_pdf, set_password
import datetime

from django.core.management import call_command
from django.http import HttpResponse


# Create your views here.

def backup(request):
    call_command("dbbackup")
    return HttpResponse('db created')


def restore(request):
    call_command("dbrestore")
    return HttpResponse('restore data')


def dumpdata(request):
    call_command("dumpdata")
    return HttpResponse('dump data')


def loaddata(request):
    call_command("loaddata")
    return HttpResponse('load data')


# Cette classe nous permet de produire des document PDF à partir d'un fichier HTML
class DownloadPDF(viewsets.ViewSet):
    def get(self, request):
        users = models.Utilisateur.objects.all()
        date = datetime.datetime.now()
        params = {
            "today": datetime.date.today(),
            "hour": "{0}h {1}min {2}s".format(date.hour, date.minute, date.second),
            "users": users,
        }
        return generateReport(params)


class GeneratePDF(viewsets.ViewSet):
    def get(self, request):
        users = models.Utilisateur.objects.all()
        date = datetime.datetime.now()
        params = {
            "today": datetime.date.today(),
            "hour": "{0}h {1}min {2}s".format(date.hour, date.minute, date.second),
            "users": users,
        }
        titre = "Liste_des_users"
        file_name, state = save_pdf(params, titre)

        if not state:
            return Response({"status": 400})

        return Response({"status": status.HTTP_200_OK, "path": f'{baseUrl()}media/pdfs/{file_name}'})


class SetPasswordViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        if set_password(request.user.id, request.data.get("newpassword")):
            return Response({'success': True, 'status': status.HTTP_200_OK,
                             'message': 'Mot de passe modifié avec succès ! Bien vouloir consulter votre boîte mail.'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'success': False, 'status': status.HTTP_400_BAD_REQUEST,
                             'message': 'Erreur de mise à jour du mot de passe'}, status=status.HTTP_400_BAD_REQUEST)


class HasPermissionViewSet(viewsets.GenericViewSet):
    '''
        Cette méthode permet de vérifier que l'utilisateur a la permission requise
    '''
    authentication_classes = [JWTAuthentication]

    def list(self, request, codename="", *args, **kwargs):
        has_perm = hasPermission(request, codename='pharmashop.{0}'.format(codename))
        if has_perm:
            return Response({'status': status.HTTP_200_OK, 'success': True, 'message':  \
                'Permission accordée'}, status=status.HTTP_200_OK)

        return Response({'status': status.HTTP_403_FORBIDDEN, 'success': False, 'message': \
            "Permission non accodée"}, status=status.HTTP_403_FORBIDDEN)


class MouvementStockForPharmacyViewSet(viewsets.GenericViewSet):
    '''
        Cette méthode permet de lister les mouvements de stock d'une pharmacie
    '''
    authentication_classes = [JWTAuthentication]

    def list(self, request, idPharmacy=None, *args, **kwargs):
        entrepots = models.Entrepot.objects.filter(pharmacie=idPharmacy)
        entrepots_ids = [e.pk for e in entrepots]
        mouvements = models.MouvementStock.objects.filter(entrepot_id__in=entrepots_ids)
        page = self.paginate_queryset(mouvements)
        serializer = serializers.MouvementStockSerializers(page, many=True)
        return self.get_paginated_response(serializer.data)


class MouvementStockForMedecineViewSet(viewsets.GenericViewSet):
    '''
        Cette méthode permet de lister les mouvements de stock d'un produit
    '''
    authentication_classes = [JWTAuthentication]

    def list(self, request, idMedecine=None, *args, **kwargs):
        mouvements = models.MouvementStock.objects.filter(medicament_id=idMedecine)
        page = self.paginate_queryset(mouvements)
        serializer = serializers.MouvementStockSerializers(page, many=True)
        return self.get_paginated_response(serializer.data)


class MouvementStockViewSet(viewsets.GenericViewSet):
    '''
        Cette méthode permet de lister et sauvegarder les mouvements de stock effectués des pharmacies
    '''
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        mouvements = models.MouvementStock.objects.all()
        page = self.paginate_queryset(mouvements)
        serializer = serializers.MouvementStockSerializers(page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = serializers.MouvementStockSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_200_OK,  'message': 'Mouvement crée avec succès', \
                             'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'results': serializer.errors}, \
                        status=status.HTTP_400_BAD_REQUEST)


class MouvementStockDetailViewSet(viewsets.ViewSet):
    '''
        Cette méthode permet de rechercher, modifier ou supprimer les information contenues dans un mouvement
    '''
    authentication_classes = [JWTAuthentication]

    def get_object(self, id):
        try:
            return models.MouvementStock.objects.get(id=id)
        except models.MouvementStock.DoesNotExist:
            return False

    def retrieve(self, request, id=None):
        mouvement = self.get_object(id)
        if mouvement:
            serializer = serializers.MouvementStockSerializers(mouvement)
            return Response({'status': status.HTTP_200_OK, 'success': True, "message": 'Mouvement trouvé', \
                             'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, \
                         'message': "Le mouvement ayant l'id={0} n'existe pas !".format(id), })

    def put(self, request, id=None):
        mouvement = self.get_object(id)
        if mouvement:
            serializer = serializers.MouvementStockSerializers(mouvement, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': status.HTTP_201_CREATED, 'success': True, \
                                 "message": 'Mise à jour effectuée avec succès', \
                                 "results": serializer.data}, status=status.HTTP_200_OK)
            return Response({'success': False, 'status': status.HTTP_400_BAD_REQUEST, \
                             "message": 'Une erreur est survenue lors de la mise à jour', \
                             'results': serializer.errors})
        return Response({'success': False, 'status': status.HTTP_404_NOT_FOUND, \
                         "message": "Le mouvement ayant l'id = {0} n'existe pas !".format(id), })

    def delete(self, request, id=None):
        mouvement = self.get_object(id)
        if mouvement:
            mouvement.delete()
            return Response({'status': status.HTTP_204_NO_CONTENT, 'success': True, \
                             'message': "Mouvement supprimé avec succès"}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'status': status.HTTP_404_NOT_FOUND, \
                         "message": "Le mouvement ayant l'id = {0} n'existe pas !".format(id), })


class InventaireForPharmacyViewSet(viewsets.GenericViewSet):
    '''
        Liste des inventaires d'une pharmacie
    '''
    authentication_classes = [JWTAuthentication]

    def list(self, request, idPharmacy=None, *args, **kwargs):
        '''
            Faire apprtenir un utilisateur à une pharmacie dans le model de la BD
            Ici récupérer la liste de utilisateur enregistrés dans la pharmacy idPharmacy \
            et passer en paramètre du filtre
        '''
        entrepots = models.Entrepot.objects.filter(pharmacie=idPharmacy)
        entrepots_ids = [e.id for e in entrepots]
        inventaires = models.Inventaire.objects.filter(entrepot__in=entrepots_ids)
        page = self.paginate_queryset(inventaires)
        serializer = serializers.InventaireSerializers(page, many=True)
        return self.get_paginated_response(serializer.data)


class InventaireViewSet(viewsets.GenericViewSet):
    '''
        Cette méthode permet de lister et sauvegarder les inventaires effectués des pharmacies
    '''
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        inventaire = models.Inventaire.objects.all()
        page = self.paginate_queryset(inventaire)
        serializer = serializers.InventaireSerializers(page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        medicaments = request.data.get('medicaments')
        serializer = serializers.InventaireSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            new_inventaire_id = serializer.data.get('id')
            for data in medicaments:
                models.InventaireMedicament(
                    inventaire=models.Inventaire.objects.get(id=new_inventaire_id),
                    medicament=models.Medicament.objects.get(id=data.get('id')),
                    quantiteAttendue=data.get('quantiteAttendue'),
                    quantiteReelle=data.get('quantiteReelle')
                ).save()

            return Response({'success': True, 'status': status.HTTP_200_OK, \
                             'message': 'Inventaire crée avec succès', 'results': serializer.data}, \
                            status=status.HTTP_200_OK)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'results': serializer.errors}, \
                        status=status.HTTP_400_BAD_REQUEST)


class InventaireDetailViewSet(viewsets.ViewSet):
    '''
        Cette méthode permet de rechercher, modifier ou supprimer les information contenues dans un entrepôt
    '''
    authentication_classes = [JWTAuthentication]

    def get_object(self, id):
        try:
            return models.Inventaire.objects.get(id=id)
        except models.Inventaire.DoesNotExist:
            return False

    def retrieve(self, request, id=None):
        inventaire = self.get_object(id)
        if inventaire:
            serializer = serializers.InventaireSerializers(inventaire)
            return Response({'status': status.HTTP_200_OK, 'success': True, \
                             "message": 'Inventaire trouvé', 'results': serializer.data}, \
                            status=status.HTTP_200_OK)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, \
                         'message': "L'inventaire ayant l'id={0} n'existe pas !".format(id), })

    def put(self, request, id=None):
        inventaire = self.get_object(id)
        if inventaire:
            serializer = serializers.InventaireSerializers(inventaire, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': status.HTTP_201_CREATED, 'success': True, \
                                 "message": 'Mise à jour effectuée avec succès', "results": serializer.data}, \
                                status=status.HTTP_200_OK)
            return Response({'success': False, 'status': status.HTTP_400_BAD_REQUEST, \
                             "message": 'Une erreur est survenue lors de la mise à jour', \
                             'results': serializer.errors})
        return Response({'success': False, 'status': status.HTTP_404_NOT_FOUND, \
                         "message": "L'inventaire ayant l'id = {0} n'existe pas !".format(id), })

    def delete(self, request, id=None):
        inventaire = self.get_object(id)
        if inventaire:
            inventaire.delete()
            return Response({'status': status.HTTP_204_NO_CONTENT, 'success': True, \
                             'message': "Inventaire supprimé avec succès"}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'status': status.HTTP_404_NOT_FOUND, \
                         "message": "L'inventaire ayant l'id = {0} n'existe pas !".format(id)})


class EntrepotForPharmacyListViewSet(viewsets.GenericViewSet):
    '''
        Cette méthode permet de lister et sauvegarder les entrepôts des pharmacies
    '''
    authentication_classes = [JWTAuthentication]

    def list(self, request, idPharmacy=None, *args, **kwargs):
        entrepots = models.Entrepot.objects.filter(pharmacie_id=idPharmacy)
        serializer = serializers.EntrepotSerializers(entrepots, many=True)
        return Response({'success': True, 'status': status.HTTP_200_OK, 'message': 'Liste des entrepôts', \
                         'results': serializer.data}, status=status.HTTP_200_OK)


class EntrepotForPharmacyViewSet(viewsets.GenericViewSet):
    '''
        Cette méthode permet de lister et sauvegarder les entrepôts des pharmacies
    '''
    authentication_classes = [JWTAuthentication]

    def list(self, request, idPharmacy=None, *args, **kwargs):
        entrepot = models.Entrepot.objects.filter(pharmacie_id=idPharmacy)
        page = self.paginate_queryset(entrepot)
        serializer = serializers.EntrepotSerializers(page, many=True)
        return self.get_paginated_response(serializer.data)


class MedicamentForEntrepotViewSet(viewsets.GenericViewSet):
    '''
        Cette méthode permet de lister et sauvegarder les entrepôts des pharmacies
    '''
    authentication_classes = [JWTAuthentication]

    def list(self, request, idEntrepot=None, *args, **kwargs):
        medicaments = models.Medicament.objects.filter(entrepot_id=idEntrepot)
        page = self.paginate_queryset(medicaments)
        serializer = serializers.MedicamentSerialisers(page, many=True)
        return self.get_paginated_response(serializer.data)


class EntrepotViewSet(viewsets.GenericViewSet):
    '''
        Cette méthode permet de lister et sauvegarder les entrepôts des pharmacies
    '''
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = serializers.EntrepotSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_200_OK, \
                             'message': 'Entrepôt crée avec succès', 'results': serializer.data}, \
                            status=status.HTTP_200_OK)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'results': serializer.errors}, \
                        status=status.HTTP_400_BAD_REQUEST)


class EntrepotDetailViewSet(viewsets.ViewSet):
    '''
        Cette méthode permet de rechercher, modifier ou supprimer les information contenues dans un entrepôt
    '''
    authentication_classes = [JWTAuthentication]

    def get_object(self, id):
        try:
            return models.Entrepot.objects.get(id=id)
        except models.Entrepot.DoesNotExist:
            return False

    def retrieve(self, request, id=None):
        entrepot = self.get_object(id)
        if entrepot:
            serializer = serializers.EntrepotDetailsSerializers(entrepot)
            return Response({'status': status.HTTP_200_OK, 'success': True, \
                             "message": 'Entrepôt trouvé', 'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, \
                         'message': "L'entrepôt ayant l'id={0} n'existe pas !".format(id), })

    def put(self, request, id=None):
        entrepot = self.get_object(id)
        if entrepot:
            serializer = serializers.EntrepotSerializers(entrepot, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': status.HTTP_201_CREATED, 'success': True, \
                                 "message": 'Mise à jour effectuée avec succès', "results": serializer.data}, \
                                status=status.HTTP_200_OK)
            return Response({'success': False, 'status': status.HTTP_400_BAD_REQUEST, \
                             "message": 'Une erreur est survenue lors de la mise à jour', \
                             'results': serializer.errors})
        return Response({'success': False, 'status': status.HTTP_404_NOT_FOUND, \
                         "message": "L'entrepôt ayant l'id = {0} n'existe pas !".format(id), })

    def delete(self, request, id=None):
        entrepot = self.get_object(id)
        if entrepot:
            entrepot.delete()
            return Response({'status': status.HTTP_204_NO_CONTENT, 'success': True, \
                             'message': "Entrepôt supprimé avec succès"}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'status': status.HTTP_404_NOT_FOUND, \
                         "message": "L'entrepôt ayant l'id = {0} n'existe pas !".format(id), })


class FactureForPharmacyViewSet(viewsets.GenericViewSet):
    '''
        Liste des factures d'une pharmacie
    '''
    authentication_classes = [JWTAuthentication]

    def list(self, request, idPharmacy=None, *args, **kwargs):
        '''
            Faire apprtenir un utilisateur à une pharmacie dans le model de la BD
            Ici récupérer la liste de utilisateur enregistrés dans la pharmacy idPharmacy \
            et passer en paramètre du filtre
        '''

        # pharmacy = models.Pharmacie.objects.get(pk=int(idPharmacy))
        factures = models.Facture.objects.filter(utilisateur__in=[request.user.id])
        page = self.paginate_queryset(factures)
        serializer = serializers.FactureSerializers(page, many=True)
        return self.get_paginated_response(serializer.data)


class FactureViewSet(viewsets.GenericViewSet):
    '''
        Cette méthode permet de lister et sauvegarder les factures des clients
    '''
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        factures = models.Facture.objects.all()
        page = self.paginate_queryset(factures)
        serializer = serializers.FactureSerializers(page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        medicaments = request.data.get('medicaments')
        if not request.data['note']:
            request.data['note'] = "Arrêter le présente facture à la somme de {0} F représentant l'achat de {1} médicament(s)." \
                .format(request.data.get('montantTotal'), request.data.get('quantiteTotal'))
        request.data['utilisateur'] = request.user.id
        serializer = serializers.FactureSerializers(data=request.data)
        if serializer.is_valid():
            ''' Création de la facture '''
            try:
                with transaction.atomic():
                    serializer.save()
                    new_facture_id = serializer.data.get('id')
                    for data in medicaments:
                        ''' Mise à jour des quantités en stock des médicaments inclus dans la facture '''
                        quantite = data.get('quantite')

                        old_medicament = models.Medicament.objects.get(id=data.get('id'))
                        old_medicament.qte_stock = old_medicament.qte_stock - quantite
                        old_medicament.save()

                        ''' Enregistrement d'une ligne de produit de la facture '''
                        models.MedicamentFacture(
                            facture=models.Facture.objects.get(id=new_facture_id),
                            medicament=old_medicament,
                            montant=data.get('prix'),
                            quantite=quantite
                        ).save()

                        ''' Enregistrement d'une sortie de stock du produit '''
                        models.MouvementStock(
                            entrepot=models.Entrepot.objects.get(id=old_medicament.entrepot_id),
                            medicament=old_medicament,
                            description="Sortie de stock du produit {0} pour le compte de la facture de référence {1} \
                             effectuée par: {2}.".format(old_medicament.nom, new_facture_id, request.user.username),
                            quantite=- quantite
                        ).save()

                    return Response({'success': True, 'status': status.HTTP_200_OK, \
                                     'message': 'Factures créée avec succès', \
                                 'lignes': len(medicaments), 'results': serializer.data}, status=status.HTTP_200_OK)

            except Exception as e:
                print(str(e))
                return Response({'success': False, 'status': status.HTTP_500_INTERNAL_SERVER_ERROR, \
                    'message': 'Une erreur est apparue. Merci de vérifier les quantités et de recommencer votre requête.', \
                    'results': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'status': status.HTTP_400_BAD_REQUEST, 'results': serializer.errors}, \
                        status=status.HTTP_400_BAD_REQUEST)


class FactureDetailViewSet(viewsets.ViewSet):
    '''
        Cette méthode permet de rechercher, modifier ou supprimer les information contenues dans une facture
    '''
    authentication_classes = [JWTAuthentication]

    def get_object(self, id):
        try:
            return models.Facture.objects.get(id=id)
        except models.Facture.DoesNotExist:
            return False

    def retrieve(self, request, id=None):
        facture = self.get_object(id)
        if facture:
            serializer = serializers.FactureSerializers(facture)
            return Response({'status': status.HTTP_200_OK, 'success': True, "message": 'Facture trouvée', \
                             'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, \
                         'message': "La Facture ayant l'id={0} n'existe pas !".format(id)})

    def put(self, request, id=None):
        facture = self.get_object(id)
        if facture:
            serializer = serializers.FactureSerializers(facture, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': status.HTTP_201_CREATED, 'success': True, \
                                 "message": 'Mise à jour effectuée avec succès', \
                                 "results": serializer.data}, status=status.HTTP_200_OK)
            return Response({'success': False, 'status': status.HTTP_400_BAD_REQUEST, \
                             "message": 'Une erreur est survenue lors de la mise à jour', \
                             'results': serializer.errors})
        return Response({'success': False, 'status': status.HTTP_404_NOT_FOUND, \
                         "message": "La facture ayant l'id = {0} n'existe pas !".format(id)})

    def delete(self, request, id=None):
        facture = self.get_object(id)
        if facture:
            facture.delete()
            return Response({'status': status.HTTP_204_NO_CONTENT, 'success': True, \
                             'message': "Facture supprimée avec succès"}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'status': status.HTTP_404_NOT_FOUND, \
                         "message": "La Facture ayant l'id = {0} n'existe pas !".format(id), })


class PharmacieProcheViewSet(viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]

    def list(self, request, rayon=0, *args, **kwargs):
        latitude = float(request.data.get('latitude', 0))  # latitude de l'utilisateur
        longitude = float(request.data.get('longitude', 0))  # longitude de l'utilisateur
        search = request.data.get('search')
        pays = request.data.get('pays')
        ville = request.data.get('ville')
        quartier = request.data.get('quartier')
        pharmacies = models.Pharmacie.objects.all()  # Liste des pharmacies
        mylist = []

        if search:
            pharmacies = pharmacies.filter(nom__icontains=search)
        if pays and ville:
            latitude, longitude = 0.0, 0.0
            pharmacies = pharmacies.filter(
                Q(localisation__icontains=pays) |
                Q(localisation__icontains=ville)
            )

        if quartier:
            latitude, longitude = 0.0, 0.0
            pharmacies = pharmacies.filter(
                Q(localisation__icontains=quartier)
            )

        if latitude != 0.0 and longitude != 0.0:
            for p in pharmacies:
                long = float(distance(latitude, p.latitude, longitude, p.longitude))
                if long <= float(rayon):
                    serializer = serializers.PharmacieSerializers(p)
                    data = serializer.data
                    data["distance"] = long
                    mylist.append(data)

        serializerdata = serializers.PharmacieSerializers(pharmacies, many=True)

        return Response({'status': status.HTTP_200_OK, 'success': True, 'message': \
            'liste des pharmacies dans un rayon {0} KM'.format(rayon), 'count': len(mylist), \
                         'results':  mylist if latitude != 0.0 and longitude != 0.0 else serializerdata.data},\
                        status=status.HTTP_200_OK)


class PharmacieFilterViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        print(request.data.get('search'))
        pharmacies = models.Pharmacie.objects.filter(nom__icontains=request.data.get('search', ''))
        serializer = serializers.PharmacieSerializers(pharmacies, many=True)
        return Response({'status': status.HTTP_200_OK, 'success': True, 'message': \
            "Liste des pharmacies", 'results': serializer.data, }, status=status.HTTP_200_OK,)


class PharmacieViewSet(viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]

    def list(self, request):
        pharmacies = models.Pharmacie.objects.all()
        page = self.paginate_queryset(pharmacies)
        serializer = serializers.PharmacieSerializers(page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        request.data['user'] = models.Utilisateur.objects.get(id=request.user.id)
        serializer = serializers.PharmacieSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_200_OK, 'message': \
                'Pharmacies créée avec succès', 'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'results': serializer.errors}, \
                        status=status.HTTP_400_BAD_REQUEST)


class PharmacieDetailViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def get_object(self, id):
        try:
            return models.Pharmacie.objects.get(id=id)
        except models.Pharmacie.DoesNotExist:
            return False

    def retrieve(self, request, id=None):

        pharmacie = self.get_object(id)
        if pharmacie:
            serializer = serializers.PharmacieSerializers(pharmacie)

            return Response({'status': status.HTTP_200_OK, 'success': True, "message": 'Pharmacie trouvée', \
                             'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, \
                         'message': "La pharmacie ayant l'id={0} n'existe pas !".format(id), })

    def put(self, request, id=None):
        pharmacie = self.get_object(id)
        if pharmacie:
            serializer = serializers.PharmacieSerializers(pharmacie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': status.HTTP_201_CREATED, 'success': True, \
                                 "message": 'Mise à jour effectuée avec succès', "results": serializer.data}, \
                                status=status.HTTP_200_OK)
            return Response({'success': False, 'status': status.HTTP_400_BAD_REQUEST, \
                             "message": 'Une erreur est survenue lors de la mise à jour', \
                             'results': serializer.errors})
        return Response({'success': False, 'status': status.HTTP_404_NOT_FOUND, \
                         "message": "la pharmacie ayant l'id = {0} n'existe pas !".format(id)})

    def delete(self, request, id=None):
        pharmacie = self.get_object(id)
        if pharmacie:
            pharmacie.delete()
            return Response({'status': status.HTTP_204_NO_CONTENT, 'success': True, \
                             'message': "Pharmacie supprimée avec succès"}, status=status.HTTP_201_CREATED)
        return Response({'success': False, 'status': status.HTTP_404_NOT_FOUND, \
                         "message": "La Pharmacie ayant l'id = {0} n'existe pas !".format(id)})


class ListPhamacieForUser(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        phamacies = models.Pharmacie.objects.filter(user_id=request.user.id)
        serializer = serializers.PharmacieSerializers(phamacies, many=True)
        return Response({'status': status.HTTP_200_OK, 'success': True, 'message': \
            "Liste des pharmacies d'un utilisateur", 'results': serializer.data, }, status=status.HTTP_200_OK, )


class CategorieViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        categorie = models.Categorie.objects.all()
        serializer = serializers.CategorieSerializers(categorie, many=True)
        return Response({'status': status.HTTP_200_OK, 'success': True, 'message': \
            'Liste des categorie', 'results': serializer.data}, status=status.HTTP_200_OK, )

    def post(self, request, *args, **kwargs):
        serializer = serializers.CategorieSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_200_OK, 'message': \
                'Catégorie crée avec succès', 'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({'success': False, 'status': status.HTTP_400_BAD_REQUEST, \
                         'results': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CategorieDetailViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def get_object(self, id):
        try:
            return models.Categorie.objects.get(id=id)
        except models.Categorie.DoesNotExist:
            return False

    def retrieve(self, request, id=None):
        categorie = self.get_object(id)
        if categorie:
            serializer = serializers.CategorieSerializers(categorie)
            return Response({"succes": True, "status": status.HTTP_200_OK, \
                             'message': 'Catégorie trouvé', "results": serializer.data}, status=status.HTTP_200_OK)
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, \
                         "message": "La catégorie ayant l'id = {0} n'existe pas !".format(id), }, \
                        status=status.HTTP_404_NOT_FOUND, )

    def put(self, request, id=None):
        categorie = self.get_object(id)
        if categorie:
            serializer = serializers.CategorieSerializers(categorie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': status.HTTP_201_CREATED, 'message': 'Mise à jour effectuée avec succès', \
                                 'success': True, 'results': serializer.data}, status=status.HTTP_201_CREATED)
            return Response({'success': False, 'status': status.HTTP_400_BAD_REQUEST, 'results': serializer.errors}, \
                            status=status.HTTP_404_NOT_FOUND)
        return Response({'success': False, 'status': status.HTTP_404_NOT_FOUND, \
                         "message": "La categorie ayant l'id = {0} n'existe pas !".format(id)}, \
                        status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id=None):
        categorie = self.get_object(id)
        if categorie:
            categorie.delete()
            return Response({'status': status.HTTP_204_NO_CONTENT, 'success': True, \
                             'message': "Categorie supprimée avec succès"}, status=status.HTTP_204_NO_CONTENT)
        return Response({'status': status.HTTP_404_NOT_FOUND, 'success': False, \
                         "message": "La categorie ayant l'id = {0} n'existe pas !".format(id)}, \
                        status=status.HTTP_404_NOT_FOUND, )


class UtilisateurViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def list(self, request):
        serializer = serializers.UtilisateurSerializer(models.Utilisateur.objects.all(), many=True)
        return Response({'success': True, 'status': status.HTTP_200_OK, 'message': \
            'liste des utilisateurs', 'results': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        if (len(data.get('username')) >= 4) and (len(data.get('password')) >= 8):
            try:
                user = models.Utilisateur.objects.create_user(
                    username=data.get('username'),
                    password=data.get('password'),
                    adresse=data.get('adresse') if data.get('adresse') else '',
                    email=data.get('email'),
                    avatar=request.FILES.get('avatar') if request.FILES.get('avatar') else '',
                    is_active=True,
                    is_staff=True if data.get('is_staff') else False,
                    is_superuser=True if data.get('is_superuser') else False,
                )
            except django.db.utils.IntegrityError as e:
                return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, \
                                 'message': "Le nom d'utilisateur '{0}' est déjà pris".format(data.get('username'))}, \
                                status=status.HTTP_400_BAD_REQUEST)

            serializer = serializers.UtilisateurSerializer(user)
            return Response({'status': status.HTTP_201_CREATED, 'success': True, \
                             'message': 'Utilisateur enrégistré avec succès', 'results': serializer.data}, \
                            status=status.HTTP_201_CREATED)

        return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, \
                         'message': 'Erreur de création de l\'utilisateur. Paramètres incomplèts !'}, \
                        status=status.HTTP_400_BAD_REQUEST)


class UtilisateurDetailViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def get_object(self, id):
        try:
            return models.Utilisateur.objects.get(id=id)
        except models.Utilisateur.DoesNotExist:
            return False

    def retrieve(self, request, id=None, *args, **kw):
        utilisateur = self.get_object(id)
        serializer = serializers.UtilisateurSerializer(utilisateur)
        if utilisateur:
            return Response({"succes": True, "status": status.HTTP_200_OK, "results": serializer.data}, \
                            status=status.HTTP_200_OK)
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, \
                         "message": "L'utilisateur ayant l'id = {0} n'existe pas !".format(id)}, \
                        status=status.HTTP_404_NOT_FOUND, )

    def put(self, request, id=None):
        utilisateur = self.get_object(id)
        if utilisateur:
            serializer = serializers.UtilisateurSerializer(utilisateur, data=request.data)
            if serializer.is_valid():
                serializer.save(is_active=True)
                return Response({'status': status.HTTP_201_CREATED, 'success': True, \
                                 "message": 'Mise à jour effectuée avec succès', "results": serializer.data}, \
                                status=status.HTTP_200_OK)
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': True, \
                             "message": 'Une erreur est survenue lors de la mise à jour', \
                             'results': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': status.HTTP_404_NOT_FOUND, 'success': True, \
                         "message": "L'utilisateur ayant l'id = {0} n'existe pas !".format(id)}, \
                        status=status.HTTP_404_NOT_FOUND, )

    def delete(self, request, id=None):
        utilisateur = self.get_object(id)
        if utilisateur:
            utilisateur.delete()
            return Response({'status': status.HTTP_204_NO_CONTENT, 'success': True, \
                             'message': "Utilisateur supprimée avec succès"}, status=status.HTTP_204_NO_CONTENT)
        return Response({'status': status.HTTP_404_NOT_FOUND, "message": \
            "L'utilisateur ayant l'id = {0} n'existe pas !".format(id)}, status=status.HTTP_404_NOT_FOUND, )


class FilterMedicamentViewSet(viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        query = request.data.get('query', [])
        medicaments = models.Medicament.objects.all().order_by("prix", "qte_stock")
        for dic in query:
            key = list(dic.keys())[0]
            if key == "position" and len(dic[key]):
                latitude = float(dic[key][0])  # latitude de l'utilisateur
                longitude = float(dic[key][1])  # longitude de l'utilisateur
                pharmacies = models.Pharmacie.objects.all()  # Liste des pharmacies
                d = dic[key][2]  # Rayon de recherche
                pharmacies_ids = []
                for p in pharmacies:
                    if float(distance(latitude, p.latitude, longitude, p.longitude)) <= float(d):
                        pharmacies_ids.append(p.pk)
                medicaments = medicaments.filter(pharmacie_id__in=pharmacies_ids)

            if key == "categorie" and dic[key]:
                if dic[key] != "Tous":
                    medicaments = medicaments.filter(categorie__libelle__icontains=dic[key])

            if key == "search" and dic[key]:
                medicaments = medicaments.filter(
                    Q(nom__icontains=dic[key]) |
                    Q(marque__icontains=dic[key]) |
                    Q(description__icontains=dic[key]) |
                    Q(categorie__libelle__icontains=dic[key]))

            if key == "voix" and len(dic[key]):
                medicaments = medicaments.filter(voix__in=dic[key])

        page = self.paginate_queryset(medicaments)
        serializer = serializers.MedicamentSerialisers(page, many=True)
        return self.get_paginated_response(serializer.data)


class MedicamentViewSet(viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]

    def list(self, request):
        medicaments = models.Medicament.objects.all().order_by("prix", "qte_stock")
        page = self.paginate_queryset(medicaments)
        serializer = serializers.MedicamentSerialisers(page, many=True)
        return self.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwarg):
        body = request.data
        data = {
            "nom": body.get('nom'),
            "prix": body.get('prix'),
            "marque": body.get('marque'),
            "date_exp": body.get('date_exp'),
            "masse": body.get('masse'),
            "qte_stock": body.get('qte_stock'),
            "posologie": body.get('posologie'),
            "categorie": body.get('categorie'),
            "pharmacie": body.get('pharmacie'),
            "description": body.get('description'),
            "voix": body.get('voix'),
            "stockAlert": body.get('stockAlert'),
            "stockOptimal": body.get('stockOptimal'),
            "entrepot": body.get('entrepot'),
            "image": body.get('image'),
            "user": models.Utilisateur.objects.get(id=request.user.id)
        }
        serializer = serializers.MedicamentSerialisers(data=data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    if data.get('image'):
                        serializer.save(image=base64_file(body.get('image')))
                    serializer.save()
                    models.HistoriquePrix(
                        basePrix=body.get('basePrix') if body.get('basePrix') else "HT",
                        tva=body.get('tva') if body.get('tva') else 19.25,
                        prixVente=body.get('prix'),
                        medicament=models.Medicament.objects.get(id=serializer.data.get('id')),
                        utilisateur=models.Utilisateur.objects.get(id=request.user.id)
                    ).save()
                    ''' Enregistrement d'une entrée de stock du produit '''
                    models.MouvementStock(
                        entrepot=models.Entrepot.objects.get(id=body.get('entrepot')),
                        medicament=models.Medicament.objects.get(id=serializer.data.get('id')),
                        description="Entrée (création) en stock du produit {0} avec pour stock initial {1}. Ajouté par: {2}." \
                            .format(body.get('nom'), body.get('qte_stock'), request.user.username),
                        quantite=body.get('qte_stock'),
                    ).save()
                    return Response({'success': True, 'status': status.HTTP_200_OK, 'message': \
                        'Médicament crée avec succès', 'results': serializer.data}, status=status.HTTP_200_OK)

            except IntegrityError as e:
                return Response({'success': False, 'status': status.HTTP_500_INTERNAL_SERVER_ERROR, \
                                 'message': 'Une erreur est apparue. Merci de recommencer votre requête.', \
                                'results': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        elif django.db.utils.IntegrityError:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, \
                             'message': \
                                 "Erreur survenue. {0} exist déjà ! \nVous pouvez juste mettre à jour votre stock. {1}". \
                            format(request.data.get('nom'), str(serializer.errors)), \
                             'results': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, \
                             'message': "Erreur de création du médicament. Paramètres incomplèts !", \
                             'results': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        # return Response({'message': 200}, status=status.HTTP_200_OK)


class MedicamentDetailViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def get_object(self, id):
        try:
            return models.Medicament.objects.get(id=id)
        except models.Medicament.DoesNotExist:
            return False

    def retrieve(self, request, id=None):
        medicament = self.get_object(id)
        serializer = serializers.MedicamentDetailSerialisers(medicament)
        if medicament:
            data = serializer.data
            data['pharmacies'] = medicament.pharmacies()
            return Response({"succes": True, "status": status.HTTP_200_OK, "message": "Médicament trouvé", \
                             "results": data}, status=status.HTTP_200_OK)
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": \
            "Le medicament ayant l'id = {0} n'existe pas !".format(id)}, status=status.HTTP_404_NOT_FOUND, )

    def put(self, request, id=None):
        medicament = self.get_object(id)
        if medicament:
            data = request.data
            data['user'] = models.Utilisateur.objects.get(pk=request.user.id)
            serializer = serializers.MedicamentSerialisers(medicament, data=data)
            if serializer.is_valid():
                newstock = request.data.get('qte_stock')
                if int(newstock) > int(medicament.qte_stock):
                    ''' Enregistrement d'une entrée de stock du produit '''
                    models.MouvementStock(
                        entrepot=models.Entrepot.objects.get(id=request.data.get('entrepot')),
                        medicament=models.Medicament.objects.get(id=int(id)),
                        description="Mise à jour du stock du produit {0}. Quantité initiale {1}, quantité finale {2}. Ajouté par: {3}." \
                            .format(request.data.get('nom'), medicament.qte_stock, newstock, request.user.username),
                        quantite=+(request.data.get('qte_stock') - int(medicament.qte_stock)),
                    ).save()
                if int(newstock) < int(medicament.qte_stock):
                    ''' Enregistrement d'une entrée de stock du produit '''
                    models.MouvementStock(
                        entrepot=models.Entrepot.objects.get(id=request.data.get('entrepot')),
                        medicament=models.Medicament.objects.get(id=int(id)),
                        description="Mise à jour du stock du produit {0}. Quantité initiale {1}, quantité finale {2}. Rétiré par: {3}." \
                            .format(request.data.get('nom'), medicament.qte_stock, newstock, request.user.username),
                        quantite=-(int(medicament.qte_stock) - request.data.get('qte_stock')),
                    ).save()
                prixMedoc = medicament.prix
                serializer.save()
                if prixMedoc != request.data.get('prix'):
                    models.HistoriquePrix(
                        basePrix=request.data.get('basePrix') if request.data.get('basePrix') else "HT",
                        tva=request.data.get('tva') if request.data.get('tva') else 19.25,
                        prixVente=request.data.get('prix'),
                        medicament=models.Medicament.objects.get(id=serializer.data.get('id')),
                        utilisateur=models.Utilisateur.objects.get(id=request.user.id)
                    ).save()

                return Response({'status': status.HTTP_201_CREATED, 'success': True, 'message': \
                    'Médicament mise à jour avec succès', "results": serializer.data}, status=status.HTTP_200_OK)
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'message': \
                'Une erreur est survenue lors de la mise à jour du médicament',
                             'results': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': status.HTTP_404_NOT_FOUND, 'success': False,
                         "message": "le medicament ayant l'id = {0} n'existe pas !".format(id)},
                        status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id=None):
        medicament = self.get_object(id)
        if medicament:
            medicament.delete()
            return Response({'status': status.HTTP_204_NO_CONTENT, 'success': True,
                             'message': "Medicament supprimée avec succès"}, status=status.HTTP_204_NO_CONTENT)
        return Response({'status': status.HTTP_404_NOT_FOUND, 'success': False,
                         "message": "Le medicament ayant l'id = {0} n'existe pas !".format(id)},
                        status=status.HTTP_404_NOT_FOUND, )


class ListMedicamentForPhamacie(viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]

    def list(self, request, id=None, *args, **kwargs):
        query = request.data.get('query', [])
        medicaments = models.Medicament.objects.filter(pharmacie__id=str(id))
        for dic in query:
            key = list(dic.keys())[0]
            if key == "categorie" and dic[key]:
                if dic[key] != "Tous":
                    medicaments = medicaments.filter(categorie__libelle__icontains=dic[key])

            if key == "search" and dic[key]:
                medicaments = medicaments.filter(
                    Q(nom__icontains=dic[key]) |
                    Q(marque__icontains=dic[key]) |
                    Q(description__icontains=dic[key]) |
                    Q(categorie__libelle__icontains=dic[key]))

            if key == "voix" and len(dic[key]):
                medicaments = medicaments.filter(voix__in=dic[key])

        page = self.paginate_queryset(medicaments)
        serializer = serializers.MedicamentSerialisers(page, many=True)
        return self.get_paginated_response(serializer.data)


class ListCategorieForMedicament(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def list(self, request, idCategorie=None, *args, **kwargs):
        listCategorie = models.Medicament.objects.filter(categorie__id=idCategorie)
        Serializer = serializers.MedicamentSerialisers(listCategorie, many=True)
        return Response({'status': status.HTTP_200_OK, 'success': True, 'message': \
            "Liste des medicaments d'une Categorie", 'results': Serializer.data}, status=status.HTTP_200_OK, )


class SymptomeViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        symptome = models.Symptome.objects.all()
        serializer = serializers.SymptomeSerializers(symptome, many=True)
        return Response({'status': status.HTTP_200_OK, 'success': True, 'message': 'Liste des symptomes', \
                         'results': serializer.data}, status=status.HTTP_200_OK, )

    def post(self, request, *args, **kwargs):
        serializer = serializers.SymptomeSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_200_OK, 'message': \
                'Sypmtome crée avec succès', 'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({'success': False, 'status': status.HTTP_400_BAD_REQUEST, \
                         'message': 'Paramètre de création imcomplèts', 'results': serializer.errors}, \
                        status=status.HTTP_400_BAD_REQUEST)


class SymptomeDetailViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def get_object(self, id):
        try:
            return models.Symptome.objects.get(id=id)
        except models.Symptome.DoesNotExist:
            return False

    def retrieve(self, request, id=None, ):
        symptome = self.get_object(id)
        if symptome:
            serializer = serializers.SymptomeSerializers(symptome)
            return Response({"succes": True, "status": status.HTTP_200_OK, 'message': 'Symptôme trouvé', \
                             "results": serializer.data}, status=status.HTTP_200_OK)
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": \
            "Le symptome ayant l'id = {0} n'existe pas !".format(id), }, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id=None):
        symptome = self.get_object(id)
        if symptome:
            serializer = serializers.SymptomeSerializers(symptome, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': status.HTTP_201_CREATED, 'message': \
                    'Mise à jour effectuée avec succès', 'success': True, 'results': serializer.data}, \
                                status=status.HTTP_201_CREATED)
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, 'message': \
                'Erreur survenue lors de la mise à jour', 'results': serializer.errors}, \
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': status.HTTP_404_NOT_FOUND, 'success': False, \
                         "message": "Le symptome ayant l'id = {0} n'existe pas !".format(id)}, \
                        status=status.HTTP_404_NOT_FOUND, )

    def delete(self, request, id=None):
        categorie = self.get_object(id)
        if categorie:
            categorie.delete()
            return Response({'status': status.HTTP_201_CREATED, 'success': True, \
                             'message': "symptome supprimée avec succès"}, status=status.HTTP_201_CREATED)
        return Response({'status': status.HTTP_404_NOT_FOUND, 'success': False, \
                         "message": "Le symptome ayant l'id = {0} n'existe pas !".format(id)}, \
                        status=status.HTTP_404_NOT_FOUND, )


class ConsultationViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        consultation = models.objectsConsultaion.objects.all()
        serializer = serializers.ConsultationSerializers(consultation, many=True)
        return Response({'status': status.HTTP_200_OK, 'success': True, 'message': 'Liste des consultations', \
                         'results': serializer.data}, status=status.HTTP_200_OK, )

    def post(self, request, *args, **kwargs):
        request.data['user'] = models.Utilisateur.objects.get(id=request.user.id)
        serializer = serializers.ConsultationSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_200_OK, 'message': \
                'Consultation crée avec succès', 'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({'success': False, 'message': 'Erreur de création ! Paramètres incomplèts', \
                         'status': status.HTTP_400_BAD_REQUEST, 'results': serializer.errors}, \
                        status=status.HTTP_400_BAD_REQUEST)


class ConsultationDetailViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def get_object(self, id):
        try:
            return models.Consultaion.objects.get(id=id)
        except models.Consultaion.DoesNotExist:
            return False

    def retrieve(self, request, id=None, ):
        consultation = self.get_object(id)
        if consultation:
            serializer = serializers.ConsultationSerializers(consultation)
            return Response({"succes": True, "status": status.HTTP_200_OK, 'message': "Consultation trouvée", \
                             "results": serializer.data}, status=status.HTTP_200_OK)
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": \
            "La consultation ayant l'id = {0} n'existe pas !".format(id)}, status=status.HTTP_404_NOT_FOUND, )

    def put(self, request, id=None):
        consultation = self.get_object(id)

        if consultation:
            serializer = serializers.ConsultationSerializers(consultation, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': status.HTTP_201_CREATED, 'message': 'Mise à jour effectuée avec succès', \
                                 'success': True, 'results': serializer.data}, status=status.HTTP_201_CREATED)
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, 'message': \
                'Erreur survenue lors de la mise à jour', 'results': serializer.errors}, \
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': status.HTTP_404_NOT_FOUND, 'success': False, \
                         "message": "La consultation ayant l'id = {0} n'existe pas !".format(id)}, \
                        status=status.HTTP_404_NOT_FOUND, )

    def delete(self, request, id=None):
        consultation = self.get_object(id)
        if consultation:
            consultation.delete()
            return Response({'status': status.HTTP_201_CREATED, 'success': True, \
                             'message': "consultation supprimée avec succès"}, status=status.HTTP_201_CREATED)
        return Response({'status': status.HTTP_404_NOT_FOUND, 'success': False, \
                         "message": "La consultation ayant l'id = {0} n'existe pas !".format(id)}, \
                        status=status.HTTP_404_NOT_FOUND, )


class ListconsultationForUser(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        listConsultation = models.Consultaion.objects.filter(user=request.user.id)
        Serializer = serializers.ConsultationSerializers(listConsultation, many=True)
        return Response({'status': status.HTTP_200_OK, 'success': True, \
                         'message': "Liste des consultations d'un utilisateur", 'results': Serializer.data}, \
                        status=status.HTTP_200_OK, )


class MaladieViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        maladie = models.Maladie.objects.all()
        serializer = serializers.MaladieSerializers(maladie, many=True)
        return Response({'status': status.HTTP_200_OK, 'success': True, 'message': 'Liste des maladies', \
                         'results': serializer.data}, status=status.HTTP_200_OK, )

    def post(self, request, *args, **kwargs):
        serializer = serializers.MaladieSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_200_OK, 'message': \
                'Maladie enregistrée avec succès', 'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({'success': False, 'status': status.HTTP_400_BAD_REQUEST, \
                         'message': 'Erreur de création ! Paramètres incomplèts', \
                         'results': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class MaladieDetailViewSet(viewsets.ViewSet):

    def get_object(self, id):
        try:
            return models.Maladie.objects.get(id=id)
        except models.Maladie.DoesNotExist:
            return False

    def retrieve(self, request, id=None, ):
        maladie = self.get_object(id)
        if maladie:
            serializer = serializers.MaladieSerializers(maladie)
            return Response({"succes": True, "status": status.HTTP_200_OK, 'message': \
                'Maladie trouvée', "results": serializer.data}, status=status.HTTP_200_OK)
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": \
            "La maladie ayant l'id = {0} n'existe pas !".format(id), }, status=status.HTTP_404_NOT_FOUND, )

    def put(self, request, id=None):
        maladie = self.get_object(id)
        if maladie:
            serializer = serializers.MaladieSerializers(maladie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': status.HTTP_201_CREATED, 'success': True, 'message': \
                    'Mise à jour effectuée avec succès', 'results': serializer.data}, status=status.HTTP_201_CREATED)
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'status': status.HTTP_400_BAD_REQUEST, \
                             'results': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': status.HTTP_404_NOT_FOUND, 'success': False, "message": \
            "La maladie ayant l'id = {0} n'existe pas !".format(id), }, status=status.HTTP_404_NOT_FOUND, )

    def delete(self, request, id=None):
        maladie = self.get_object(id)
        if maladie:
            maladie.delete()
            return Response({'status': status.HTTP_201_CREATED, 'success': True, \
                             'message': "consultation supprimée avec succès"}, status=status.HTTP_201_CREATED)
        return Response({'status': status.HTTP_404_NOT_FOUND, 'success': False, \
                         "message": "La consultation ayant l'id = {0} n'existe pas !".format(id)}, \
                        status=status.HTTP_404_NOT_FOUND, )


class DetailMedicamentViewset(viewsets.ViewSet):

    def get_object(self, id):
        try:
            return models.Medicament.objects.get(id=id)
        except models.Medicament.DoesNotExist:
            return False

    def retrieve(self, request, id=None, *args, **kw):

        medicament = self.get_object(id)
        if medicament:
            serializer = serializers.MedicamentDetailSerialisers(medicament)
            data = serializer.data
            return Response({'success': True, 'status': status.HTTP_200_OK, \
                             "message": "Détail du medicament", 'results': data})
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, \
                         "message": "Le medicament ayant l'id = {0} n'existe pas !".format(id)}, \
                        status=status.HTTP_404_NOT_FOUND)


class CarnetViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        carnet = models.Carnet.objects.all()
        serializer = serializers.CarnetSerializers(carnet, many=True)
        return Response({'status': status.HTTP_200_OK, 'success': True, 'message': 'Liste des maladies', \
                         'results': serializer.data}, status=status.HTTP_200_OK, )

    def post(self, request, *args, **kwargs):
        serializer = serializers.CarnetSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_200_OK, 'message': \
                'Carnet crée avec succès', 'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, \
                         'message': 'Erreur de création ! Paramètres incomplèts', 'results': serializer.errors}, \
                        status=status.HTTP_400_BAD_REQUEST)


class CarnetDetailViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def get_object(self, id):
        try:
            return models.Carnet.objects.get(id=id)
        except models.Carnet.DoesNotExist:
            return False

    def retrieve(self, request, id=None, ):
        carnet = self.get_object(id)
        if carnet:
            serializer = serializers.CarnetSerializers(carnet)
            return Response({"succes": True, "status": status.HTTP_200_OK, 'message': 'Cartnet trouvé', \
                             "results": serializer.data}, status=status.HTTP_200_OK)
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": \
            "La carnet ayant l'id = {0} n'existe pas !".format(id), }, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id=None):
        carnet = self.get_object(id)

        if carnet:
            serializer = serializers.CarnetSerializers(carnet, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': status.HTTP_201_CREATED, 'success': True, \
                                 'message': 'Mise a jour effectuée avec succès', 'success': True, \
                                 'results': serializer.data}, status=status.HTTP_201_CREATED)
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, 'message': \
                'Erreur de création ! Paramètres incomplèts', 'results': serializer.errors}, \
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': status.HTTP_404_NOT_FOUND, 'success': False, \
                         "message": "Le carnet ayant l'id = {0} n'existe pas !".format(id)}, \
                        status=status.HTTP_404_NOT_FOUND, )

    def delete(self, request, id=None):
        maladie = self.get_object(id)
        if maladie:
            maladie.delete()
            return Response({'status': status.HTTP_201_CREATED, 'success': True, \
                             'message': "Carnet supprimée avec succès"}, status=status.HTTP_201_CREATED)
        return Response({'status': status.HTTP_404_NOT_FOUND, 'success': False, "message": \
            "La carnet ayant l'id = {0} n'existe pas !".format(id)}, status=status.HTTP_404_NOT_FOUND, )


class CarnetForUser(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def carnet(self, request, *args, **kwargs):
        carnet = models.Carnet.objects.filter(user=request.user.id)
        serializer = serializers.CarnetSerializers(carnet, many=True)
        return Response({'status': status.HTTP_200_OK, 'success': True, 'message': "Carnet d'un utilisateur", \
                         'results': serializer.data, }, status=status.HTTP_200_OK, )
