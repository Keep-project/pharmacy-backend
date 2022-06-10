from distutils.log import error
from msilib.schema import ServiceInstall
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Carnet, Symptome,Utilisateur,Categorie,\
    Pharmacie,Medicament

from .serializers import PharmacieSerializers,SymptomeSerializers,UtilisateurSerializer,\
    CategorieSerializers,MedicamentSerialisers
from pharmashop import serializers   


# Create your views here.


class PharmacieViewSet(viewsets.ViewSet):
    def list(self, request):

        
        pharmacie = Pharmacie.objects.all()
        Serializer = PharmacieSerializers(pharmacie, many=True)
        return Response({'status': status.HTTP_200_OK,'success': True,'message': 'Liste des pharmacies','results': Serializer.data,},status=status.HTTP_200_OK,)


    def post(self, request, *args, **kwargs):
        serializer = PharmacieSerializers(data=request.data)
        if serializer.is_valid():
                
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_200_OK, 'message': 'Catégorie créée avec succès', 'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors }, status=status.HTTP_400_BAD_REQUEST)    

    # def post(request, self, *args, **kwarg):
    #     serializer = PharmacieSerializers(data = request.data)
    #     if serializer.is_valid():
    #         pharmacie = Pharmacie(
    #             nom = request.data.get('nom'),
    #             localisation = request.data.get('localisation'),
    #             tel = request.data.get('tel'),
    #             latitude = request.data.get('latitude'),
    #             longitude = request.data.get('longitude'),
    #             h_ouverture = request.data.get('h_ouverture'),
    #             h_fermeture = request.data.get('h_fermeture'),
    #             user = request.data.get('user')

    #         )
    #         pharmacie.save()
    #         serializer = PharmacieSerializers

    #     return Response({'status': status.HTTP_200_OK,'success': True,'message': 'Pharmacie crée avec success','results': serializer.data,},status=status.HTTP_200_OK,)
        # return Response({'status': status.HTTP_200_OK,'success': True,'message': 'error','results': error(),},status=status.HTTP_404_NOT_FOUND,)


class CategorieViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        # Utilisateur.objects.create(
        #     password= "jenifer",
        #     username= "jenifer",
        #     email= "jenifer@gmail.com"
        # )
        categorie = Categorie.objects.all()
        serializer = CategorieSerializers(categorie, many=True)
        return Response({'status': status.HTTP_200_OK,'success': True,'message': 'Liste des categorie', 'results':serializer.data},status=status.HTTP_200_OK,)

    def post(self, request, *args, **kwargs):
        
        serializer = CategorieSerializers(data=request.data)
        if serializer.is_valid():
            
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_200_OK, 'message': 'Catégorie crée avec succès', 'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors }, status=status.HTTP_400_BAD_REQUEST)


class UtilisateurViewSet(viewsets.ViewSet):
    def list(request, self):
        utilisateur = Utilisateur.objects.all()
        serializer = UtilisateurSerializer(utilisateur, many=True)
        return Response({'success': True, 'status':status.HTTP_200_OK, 'message': 'liste des utilisateurs','results':serializer.data}, status=status.HTTP_200_OK)


    def post(self,request, *args, **kwarg):
        serializer = UtilisateurSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():

            
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_201_CREATED, 'message': 'utilisateur crée avec success', 'results':serializer.data}, status = status.HTTP_201_CREATED)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors }, status=status.HTTP_400_BAD_REQUEST)        


  


