


from tracemalloc import start
from requests import request
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

import django

from .models import Maladie, Utilisateur,Categorie,\
    Pharmacie,Medicament,Symptome,Consultaion,Carnet


# Create your views here.


from .serializers import PharmacieSerializers,UtilisateurSerializer,\
    CategorieSerializers,MedicamentSerialisers,SymptomeSerializers,\
    ConsultationSerializers,MaladieSerializers, CarnetSerializers    
   


# Create your views here.


class PharmacieViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    def list(self, request):
        pharmacie = Pharmacie.objects.all()
        Serializer = PharmacieSerializers(pharmacie, many=True)
        return Response({'status': status.HTTP_200_OK,'success': True,'message': 'Liste des pharmacies','results': Serializer.data,},status=status.HTTP_200_OK,)


    def post(self, request, *args, **kwargs):
        serializer = PharmacieSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_200_OK, 'message': 'pharmacies créée avec succès', 'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'results': serializer.errors }, status=status.HTTP_400_BAD_REQUEST)

class PharmacieDetailViewSet(viewsets.ViewSet):
    def get_object(self, id):
        try:
           return Pharmacie.objects.get(id=id)
        except Pharmacie.DoesNotExist:
             return False

    def retrieve(self, request,id=None):
        pharmacie = self.get_object(id)  
        if pharmacie:
            serializer = PharmacieSerializers(pharmacie)
            return Response({'status':status.HTTP_200_OK, 'success': True, "message" : 'Pharmacie trouvée', 'results':serializer.data}, status=status.HTTP_200_OK) 
        return Response({'status': status.HTTP_400_BAD_REQUEST,'success': False, 'message':"La pharmacie ayant l'id={0} n'existe pas !".format(id), })          

    def put(self, request,id=None):
        pharmacie = self.get_object(id)
        if pharmacie:
            serializer = PharmacieSerializers(pharmacie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': status.HTTP_201_CREATED,'success': True,  "message" : 'Mise à jour effectuée avec succès', "results":serializer.data}, status=status.HTTP_200_OK)
            return Response({ 'success': False, 'status': status.HTTP_400_BAD_REQUEST,  "message" : 'Une erreur est survenue lors de la mise à jour', 'results': serializer.errors})
        return Response({'success': False, 'status': status.HTTP_404_NOT_FOUND, "message":"la pharmacie ayant l'id = {0} n'existe pas !".format(id),})        
                            
    def delete(self, request, id=None):
        pharmacie = self.get_object(id)
        if pharmacie:
            pharmacie.delete()
            return Response({'status':status.HTTP_204_NO_CONTENT, 'success':True, 'message':"Pharmacie supprimée avec succès"},status=status.HTTP_201_CREATED)
        return Response({'success' : False, 'status': status.HTTP_404_NOT_FOUND, "message":"La Pharmacie ayant l'id = {0} n'existe pas !".format(id),})    

class ListPhamacieForUser(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        listPhamacie = Pharmacie.objects.filter(user=request.user.id)
        Serializer = PharmacieSerializers(listPhamacie, many=True)
        return Response({'status': status.HTTP_200_OK,'success': True,'message': "Liste des pharmacies d'un utilisateur",'results': Serializer.data,},status=status.HTTP_200_OK,)

   
class CategorieViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        categorie = Categorie.objects.all()
        serializer = CategorieSerializers(categorie, many=True)
        return Response({'status': status.HTTP_200_OK, 'success': True, 'message': 'Liste des categorie', 'results': serializer.data}, status=status.HTTP_200_OK,)

    def post(self, request, *args, **kwargs):
        serializer = CategorieSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_200_OK, 'message': 'Catégorie crée avec succès', 'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({'success': False, 'status': status.HTTP_400_BAD_REQUEST, 'results': serializer.errors }, status=status.HTTP_400_BAD_REQUEST)

class CategorieDetailViewSet(viewsets.ViewSet):
    def get_object(self,id):
        try:
            return Categorie.objects.get(id=id)
        except Categorie.DoesNotExist:
                return False  
                 
    def retrieve(self, request, id=None,):
        categorie = self.get_object(id)
        if categorie:
            serializer = CategorieSerializers(categorie)
            return Response({"succes": True, "status": status.HTTP_200_OK, "results": serializer.data}, status=status.HTTP_200_OK)
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "La catégorie ayant l'id = {0} n'existe pas !".format(id), }, status=status.HTTP_404_NOT_FOUND,)
    
    def put(self,request,id=None):
        categorie = self.get_object(id)
        if categorie:
            serializer = CategorieSerializers(categorie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':status.HTTP_201_CREATED, 'success':True, 'results': serializer.data},status=status.HTTP_201_CREATED)
            return Response({'success': False, 'status': status.HTTP_400_BAD_REQUEST, 'results': serializer.errors}, status=status.HTTP_404_NOT_FOUND) 
        return Response({'success': False, 'status':status.HTTP_404_NOT_FOUND, "message":"La categorie ayant l'id = {0} n'existe pas !".format(id),}, status=status.HTTP_404_NOT_FOUND)       

    def delete(self, request, id=None):
        categorie = self.get_object(id)
        if categorie:
            categorie.delete()
            return Response({'status':status.HTTP_204_NO_CONTENT, 'success':True, 'message':"Categorie supprimée avec succès"}, status=status.HTTP_204_NO_CONTENT)
        return Response({'status': status.HTTP_404_NOT_FOUND, 'success':False,  "message":"La categorie ayant l'id = {0} n'existe pas !".format(id),}, status=status.HTTP_404_NOT_FOUND,)       
          

class UtilisateurViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    def list(self, request):
        utilisateur = Utilisateur.objects.all()
        serializer = UtilisateurSerializer(utilisateur, many=True)
        return Response({'success': True, 'status':status.HTTP_200_OK, 'message': 'liste des utilisateurs','results':serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        if ((len(data.get('username')) >= 4) and (len(data.get('password')) >= 8)):
            try:
                user = Utilisateur.objects.create_user(
                username= data.get('username'),
                password= data.get('password'),
                adresse = data.get('adresse'),
                email= data.get('email'),
                avatar= request.FILES.get('avatar') if request.FILES.get('avatar') else '',
                is_active=True,
                is_staff=True,
                is_superuser=  True if data.get('is_superuser') else False,
            )
            except django.db.utils.IntegrityError as e:
               return Response({'status': status.HTTP_400_BAD_REQUEST, 'success' : False, 'message': "Le nom d'utilisateur '{0}' est déjà pris".format(data.get('username')) }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = UtilisateurSerializer(user)
            return Response({'status': status.HTTP_201_CREATED, 'success': True, 'message': 'Utilisateur enrégistré avec succès', 'results': serializer.data}, status=status.HTTP_201_CREATED)

        return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, 'message': 'Erreur de création de l\'utilisateur. Paramètres incomplèts !',} ,status=status.HTTP_400_BAD_REQUEST)

        
class UtilisateurDetailViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    def get_object(self, id):
        try:
            return Utilisateur.objects.get(id=id)
        except Utilisateur.DoesNotExist:
            return False

    def retrieve(self,request,id=None, *args, **kw):
        utilisateur = self.get_object(id) 
        serializer = UtilisateurSerializer(utilisateur)
        if utilisateur:
            return Response({"succes": True, "status": status.HTTP_200_OK, "results": serializer.data}, status=status.HTTP_200_OK)
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "L'utilisateur ayant l'id = {0} n'existe pas !".format(id), }, status=status.HTTP_404_NOT_FOUND,)

    def put(self, request,id=None):
        utilisateur = self.get_object(id)
        if utilisateur:
            serializer = UtilisateurSerializer(utilisateur, data=request.data)
            if serializer.is_valid():
                serializer.save(is_active= True)
                return Response({'status': status.HTTP_201_CREATED,'success': True, "message" : 'Mise à jour effectuée avec succès',  "results": serializer.data}, status=status.HTTP_200_OK)
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': True,  "message" : 'Une erreur est survenue lors de la mise à jour', 'results': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': status.HTTP_404_NOT_FOUND, 'success': True, "message": "L'utilisateur ayant l'id = {0} n'existe pas !".format(id),}, status=status.HTTP_404_NOT_FOUND,)

    def delete(self, request, id=None):
        utilisateur = self.get_object(id)
        if utilisateur:
            utilisateur.delete()
            return Response({'status':status.HTTP_204_NO_CONTENT, 'success':True, 'message':"Utilisateur supprimée avec succès"},status=status.HTTP_204_NO_CONTENT)
        return Response({'status':status.HTTP_404_NOT_FOUND, "message": "L'utilisateur ayant l'id = {0} n'existe pas !".format(id),}, status=status.HTTP_404_NOT_FOUND,)


class MedicamentViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    def list(self, request):
        medicament = Medicament.objects.all()
        serializer = MedicamentSerialisers(medicament, many=True)
        return Response({'success': True, 'status':status.HTTP_200_OK, 'message': 'liste des medicaments','results':serializer.data}, status=status.HTTP_200_OK)


    def post(self,request, *args, **kwarg):
        serializer = MedicamentSerialisers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_201_CREATED, 'message': 'Medicament crée avec succès', 'results':serializer.data}, status = status.HTTP_201_CREATED)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, 'message': "Erreur de création d'un médicament. Paramètres incomplèts !", 'results': serializer.errors} ,status=status.HTTP_400_BAD_REQUEST)


class MedicamentDetailViewSet(viewsets.ViewSet):
    def get_object(self, id):
        try:
            return Medicament.objects.get(id=id)
        except Medicament.DoesNotExist:
            return False

    def retrieve(self,request,id=None):
        medicament = self.get_object(id) 
        serializer = MedicamentSerialisers(medicament) 
        if medicament:
            return Response({"succes": True, "status": status.HTTP_200_OK, "message": "Médicament trouvé" ,"results": serializer.data}, status=status.HTTP_200_OK)
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "Le medicament ayant l'id = {0} n'existe pas !".format(id),}, status=status.HTTP_404_NOT_FOUND,)

    def put(self, request,id=None):
        medicament = self.get_object(id)
        if medicament:
            serializer = MedicamentSerialisers(medicament, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': status.HTTP_201_CREATED,'success': True, 'message': 'Médicament mise à jour avec succès', "results":serializer.data}, status=status.HTTP_200_OK)
            return Response({'status': status.HTTP_400_BAD_REQUEST,  'message': 'Une erreur est survenue lors de la mise à jour du médicament', 'results': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': status.HTTP_404_NOT_FOUND, 'success': False, "message":"le medicament ayant l'id = {0} n'existe pas !".format(id),}, status=status.HTTP_404_NOT_FOUND,)        

    def delete(self, request, id=None):
        medicament = self.get_object(id)
        if medicament:
            medicament.delete()
            return Response({'status':status.HTTP_204_NO_CONTENT, 'success':True, 'message':"Medicament supprimée avec succès"},status=status.HTTP_204_NO_CONTENT)
        return Response({'status':status.HTTP_404_NOT_FOUND, 'success': False,"message":"Le medicament ayant l'id = {0} n'existe pas !".format(id),}, status=status.HTTP_404_NOT_FOUND,)
class ListMedicamentForPhamacie(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    def list(self, request, idPharmacie=None, *args, **kwargs):
        listmedicament = Medicament.objects.filter(pharmacie__id=int(idPharmacie))
        Serializer = MedicamentSerialisers(listmedicament, many=True)
        return Response({'status': status.HTTP_200_OK,'success': True,'message': "liste des médicaments d'une pharmacie",'results': Serializer.data,},status=status.HTTP_200_OK,)

class ListCategorieForMedicament(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def list(self, request, idCategorie=None, *args, **kwargs):
        listCategorie = Medicament.objects.filter(categorie__id=idCategorie)
        Serializer = MedicamentSerialisers(listCategorie, many=True)
        return Response({ 'status': status.HTTP_200_OK, 'success': True, 'message': "Liste des medicaments d'une Categorie  ", 'results': Serializer.data,},status=status.HTTP_200_OK,)

class SymptomeViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        symptome = Symptome.objects.all()
        serializer = SymptomeSerializers(symptome, many=True)
        return Response({'status': status.HTTP_200_OK,'success': True,'message': 'Liste des symptomes', 'results':serializer.data},status=status.HTTP_200_OK,)

    def post(self, request, *args, **kwargs):
        
        serializer = SymptomeSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_200_OK, 'message': 'Sypmtome crée avec succès', 'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({ 'success': False, 'status': status.HTTP_400_BAD_REQUEST, 'message': 'Paramètre de création imcomplèts',  'results': serializer.errors, }, status=status.HTTP_400_BAD_REQUEST)


class SymptomeDetailViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    def get_object(self,id):
        try:
            return Symptome.objects.get(id=id)
        except Symptome.DoesNotExist:
                return False  
                 
    def retrieve(self, request, id=None,):
        symptome = self.get_object(id)
        if symptome:
            serializer = SymptomeSerializers(symptome)
            return Response({"succes": True, "status": status.HTTP_200_OK, 'message': 'Symptôme trouvé', "results": serializer.data}, status=status.HTTP_200_OK)
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "Le symptome ayant l'id = {0} n'existe pas !".format(id), }, status=status.HTTP_404_NOT_FOUND,)
    
    def put(self,request,id=None):
        symptome = self.get_object(id)
        
        if symptome:
            serializer = SymptomeSerializers(symptome, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':status.HTTP_201_CREATED, 'message': 'Mise à jour effectuée avec succès', 'success':True, 'results':serializer.data},status=status.HTTP_201_CREATED)
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, 'message': 'Erreur survenue lors de la mise à jour', 'results': serializer.errors}, status=status.HTTP_400_BAD_REQUEST) 
        return Response({'status':status.HTTP_404_NOT_FOUND, 'success': False, ''"message":"Le symptome ayant l'id = {0} n'existe pas !".format(id),}, status=status.HTTP_404_NOT_FOUND,)       

    def delete(self, request, id=None):
        categorie = self.get_object(id)
        if categorie:
            categorie.delete()
            return Response({'status':status.HTTP_201_CREATED, 'success':True, 'message':"symptome supprimée avec succès"},status=status.HTTP_201_CREATED)
        return Response({'status':status.HTTP_404_NOT_FOUND, 'success': False, "message":"Le symptome ayant l'id = {0} n'existe pas !".format(id),}, status=status.HTTP_404_NOT_FOUND,) 



class ConsultationViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    def list(self, request, *args, **kwargs):
       
        consultation = Consultaion.objects.all()
        serializer = ConsultationSerializers(consultation, many=True)
        return Response({'status': status.HTTP_200_OK,'success': True,'message': 'Liste des consultations', 'results':serializer.data},status=status.HTTP_200_OK,)

    def post(self, request, *args, **kwargs):
        
        serializer = ConsultationSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_200_OK, 'message': 'Consultation crée avec succès', 'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({ 'success': False, 'message' : 'Erreur de création ! Paramètres incomplèts','status': status.HTTP_400_BAD_REQUEST, 'results': serializer.errors }, status=status.HTTP_400_BAD_REQUEST) 


class ConsultationDetailViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    def get_object(self,id):
        try:
            return Consultaion.objects.get(id=id)
        except Consultaion.DoesNotExist:
                return False  
                 
    def retrieve(self, request, id=None,):
        consultation = self.get_object(id)
        if consultation:
            serializer = ConsultationSerializers(consultation)
            return Response({"succes": True, "status": status.HTTP_200_OK, 'message': "Consultation trouvée", "results": serializer.data}, status=status.HTTP_200_OK)
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "La consultation ayant l'id = {0} n'existe pas !".format(id), }, status=status.HTTP_404_NOT_FOUND,)
    
    def put(self,request,id=None):
        consultation = self.get_object(id)
        
        if consultation:
            serializer = ConsultationSerializers(consultation, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':status.HTTP_201_CREATED, 'message': 'Mise à jour effectuée avec succès', 'success':True, 'results':serializer.data},status=status.HTTP_201_CREATED)
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, 'message': 'Erreur survenue lors de la mise à jour','results': serializer.errors}, status=status.HTTP_400_BAD_REQUEST) 
        return Response({'status':status.HTTP_404_NOT_FOUND, 'success':False, "message":"La consultation ayant l'id = {0} n'existe pas !".format(id),}, status=status.HTTP_404_NOT_FOUND,)       

    def delete(self, request, id=None):
        consultation = self.get_object(id)
        if consultation:
            consultation.delete()
            return Response({'status':status.HTTP_201_CREATED, 'success':True, 'message':"consultation supprimée avec succès"},status=status.HTTP_201_CREATED)
        return Response({'status':status.HTTP_404_NOT_FOUND, 'success': False, "message":"La consultation ayant l'id = {0} n'existe pas !".format(id),}, status=status.HTTP_404_NOT_FOUND,)                           


class ListconsultationForUser(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    def list(self, request, *args, **kwargs):
        listConsultation = Consultaion.objects.filter(user=request.user.id)
        Serializer = ConsultationSerializers(listConsultation, many=True)
        return Response({'status': status.HTTP_200_OK,'success': True,'message': "Liste des consultations d'un utilisateur",'results': Serializer.data,},status=status.HTTP_200_OK,)    

class MaladieViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    def list(self, request, *args, **kwargs):
        maladie = Maladie.objects.all()
        serializer = MaladieSerializers(maladie, many=True)
        return Response({'status': status.HTTP_200_OK,'success': True,'message': 'Liste des maladies', 'results':serializer.data},status=status.HTTP_200_OK,)

    def post(self, request, *args, **kwargs):
        serializer = MaladieSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_200_OK, 'message': 'Maladie enregistrée avec succès', 'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({ 'success': False, 'status': status.HTTP_400_BAD_REQUEST, 'message' : 'Erreur de création ! Paramètres incomplèts', 'results': serializer.errors }, status=status.HTTP_400_BAD_REQUEST)


class MaladieDetailViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    def get_object(self,id):
        try:
            return Maladie.objects.get(id=id)
        except Maladie.DoesNotExist:
                return False  
                 
    def retrieve(self, request, id=None,):
        maladie = self.get_object(id)
        if maladie:
            serializer = MaladieSerializers(maladie)
            return Response({"succes": True, "status": status.HTTP_200_OK, 'message': 'Maladie trouvée', "results": serializer.data}, status=status.HTTP_200_OK)
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "La maladie ayant l'id = {0} n'existe pas !".format(id), }, status=status.HTTP_404_NOT_FOUND,)
    
    def put(self,request,id=None):
        maladie = self.get_object(id)
        if maladie:
            serializer = MaladieSerializers(maladie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':status.HTTP_201_CREATED, 'success':True, 'message': 'Mise à jour effectuée avec succès', 'results':serializer.data},status=status.HTTP_201_CREATED)
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'status': status.HTTP_400_BAD_REQUEST, 'results': serializer.errors}, status=status.HTTP_400_BAD_REQUEST) 
        return Response({'status':status.HTTP_404_NOT_FOUND, 'success':False, "message":"La maladie ayant l'id = {0} n'existe pas !".format(id),}, status=status.HTTP_404_NOT_FOUND,)       

    def delete(self, request, id=None):
        maladie = self.get_object(id)
        if maladie:
            maladie.delete()
            return Response({'status':status.HTTP_201_CREATED, 'success':True, 'message':"consultation supprimée avec succès"},status=status.HTTP_201_CREATED)
        return Response({'status':status.HTTP_404_NOT_FOUND, 'success': False,"message":"La consultation ayant l'id = {0} n'existe pas !".format(id),}, status=status.HTTP_404_NOT_FOUND,)                           

        
class CarnetViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    def list(self, request, *args, **kwargs):
        carnet = Carnet.objects.all()
        serializer = CarnetSerializers(carnet, many=True)
        return Response({'status': status.HTTP_200_OK,'success': True,'message': 'Liste des maladies', 'results':serializer.data},status=status.HTTP_200_OK,)

    def post(self, request, *args, **kwargs):
        serializer = CarnetSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_200_OK, 'message': 'Carnet crée avec succès', 'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, 'message':'Erreur de création ! Paramètres incomplèts', 'results': serializer.errors }, status=status.HTTP_400_BAD_REQUEST)



class  CaranetDetailViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    def get_object(self,id):
        try:
            return Carnet.objects.get(id=id)
        except Carnet.DoesNotExist:
                return False  
                 
    def retrieve(self, request, id=None,):
        carnet = self.get_object(id)
        if carnet:
            serializer = CarnetSerializers(carnet)
            return Response({"succes": True, "status": status.HTTP_200_OK, 'message': 'Cartnet trouvé', "results": serializer.data}, status=status.HTTP_200_OK)
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "La carnet ayant l'id = {0} n'existe pas !".format(id), }, status=status.HTTP_404_NOT_FOUND,)
    
    def put(self,request,id=None):
        carnet = self.get_object(id)
        
        if carnet:
            serializer = CarnetSerializers(carnet, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':status.HTTP_201_CREATED, 'success': True, 'message':'Mise a jour effectuée avec succès','success':True, 'results':serializer.data}, status=status.HTTP_201_CREATED)
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, 'message':'Erreur de création ! Paramètres incomplèts', 'results': serializer.errors}, status=status.HTTP_400_BAD_REQUEST) 
        return Response({'status':status.HTTP_404_NOT_FOUND, 'success': False, "message": "Le carnet ayant l'id = {0} n'existe pas !".format(id),}, status=status.HTTP_404_NOT_FOUND,)       

    def delete(self, request, id=None):
        maladie = self.get_object(id)
        if maladie:
            maladie.delete()
            return Response({'status':status.HTTP_201_CREATED, 'success':True, 'message':"Carnet supprimée avec succès"},status=status.HTTP_201_CREATED)
        return Response({'status':status.HTTP_404_NOT_FOUND, 'success': False, "message":"La carnet ayant l'id = {0} n'existe pas !".format(id),}, status=status.HTTP_404_NOT_FOUND,)                           

class CarnetForUser(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    def carnet(self, request, *args, **kwargs):
        carnet = Carnet.objects.filter(user=request.user.id)
        serializer = CarnetSerializers(carnet, many=True)
        return Response({'status': status.HTTP_200_OK,'success': True,'message': "Carnet d'un utilisateur",'results': serializer.data,},status=status.HTTP_200_OK,)