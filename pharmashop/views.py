
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
import django

from pharmashop import models, serializers


# Create your views here.


class PharmacieViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    def list(self, request):
        pharmacie = models. Pharmacie.objects.all()
        Serializer = serializers.PharmacieSerializers(pharmacie, many=True)
        return Response({'status': status.HTTP_200_OK,'success': True,'message': 'Liste des pharmacies','results': Serializer.data,},status=status.HTTP_200_OK,)


    def post(self, request, *args, **kwargs):
        serializer = serializers.PharmacieSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_200_OK, 'message': 'pharmacies créée avec succès', 'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'results': serializer.errors }, status=status.HTTP_400_BAD_REQUEST)

class PharmacieDetailViewSet(viewsets.ViewSet):
    def get_object(self, id):
        try:
           return models.Pharmacie.objects.get(id=id)
        except models.Pharmacie.DoesNotExist:
             return False

    def retrieve(self, request,id=None):
        pharmacie = self.get_object(id)  
        if pharmacie:
            serializer = serializers.PharmacieSerializers(pharmacie)
            return Response({'status':status.HTTP_200_OK, 'success': True, "message" : 'Pharmacie trouvée', 'results':serializer.data}, status=status.HTTP_200_OK) 
        return Response({'status': status.HTTP_400_BAD_REQUEST,'success': False, 'message':"La pharmacie ayant l'id={0} n'existe pas !".format(id), })          

    def put(self, request,id=None):
        pharmacie = self.get_object(id)
        if pharmacie:
            serializer = models.PharmacieSerializers(pharmacie, data=request.data)
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
        listPhamacie = models.Pharmacie.objects.filter(user=request.user.id)
        Serializer = serializers.PharmacieSerializers(listPhamacie, many=True)
        return Response({'status': status.HTTP_200_OK,'success': True,'message': "Liste des pharmacies d'un utilisateur",'results': Serializer.data,},status=status.HTTP_200_OK,)

   
class CategorieViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        categorie = models.Categorie.objects.all()
        serializer = serializers.CategorieSerializers(categorie, many=True)
        return Response({'status': status.HTTP_200_OK, 'success': True, 'message': 'Liste des categorie', 'results': serializer.data}, status=status.HTTP_200_OK,)

    def post(self, request, *args, **kwargs):
        serializer = serializers.CategorieSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_200_OK, 'message': 'Catégorie crée avec succès', 'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({'success': False, 'status': status.HTTP_400_BAD_REQUEST, 'results': serializer.errors }, status=status.HTTP_400_BAD_REQUEST)

class CategorieDetailViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    def get_object(self,id):
        try:
            return models.Categorie.objects.get(id=id)
        except models.Categorie.DoesNotExist:
                return False  
                 
    def retrieve(self, request, id=None,):
        categorie = self.get_object(id)
        if categorie:
            serializer = serializers.CategorieSerializers(categorie)
            return Response({"succes": True, "status": status.HTTP_200_OK, 'message': 'Catégorie trouvé' ,"results": serializer.data}, status=status.HTTP_200_OK)
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "La catégorie ayant l'id = {0} n'existe pas !".format(id), }, status=status.HTTP_404_NOT_FOUND,)
    
    def put(self,request,id=None):
        categorie = self.get_object(id)
        if categorie:
            serializer = serializers.CategorieSerializers(categorie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':status.HTTP_201_CREATED, 'message': 'Mise à jour effectuée avec succès', 'success':True, 'results': serializer.data},status=status.HTTP_201_CREATED)
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
        utilisateur = models.Utilisateur.objects.all()
        serializer = serializers.UtilisateurSerializer(utilisateur, many=True)
        return Response({'success': True, 'status':status.HTTP_200_OK, 'message': 'liste des utilisateurs','results':serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        if ((len(data.get('username')) >= 4) and (len(data.get('password')) >= 8)):
            try:
                user = models.Utilisateur.objects.create_user(
                username= data.get('username'),
                password= data.get('password'),
                adresse = data.get('adresse') if data.get('adresse') else '',
                email= data.get('email'),
                avatar= request.FILES.get('avatar') if request.FILES.get('avatar') else '',
                is_active=True,
                is_staff=True,
                is_superuser=  True if data.get('is_superuser') else False,
            )
            except django.db.utils.IntegrityError as e:
               return Response({'status': status.HTTP_400_BAD_REQUEST, 'success' : False, 'message': "Le nom d'utilisateur '{0}' est déjà pris".format(data.get('username')) }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer = serializers.UtilisateurSerializer(user)
            return Response({'status': status.HTTP_201_CREATED, 'success': True, 'message': 'Utilisateur enrégistré avec succès', 'results': serializer.data}, status=status.HTTP_201_CREATED)

        return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, 'message': 'Erreur de création de l\'utilisateur. Paramètres incomplèts !',} ,status=status.HTTP_400_BAD_REQUEST)

        
class UtilisateurDetailViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    def get_object(self, id):
        try:
            return models.Utilisateur.objects.get(id=id)
        except models.Utilisateur.DoesNotExist:
            return False

    def retrieve(self,request,id=None, *args, **kw):
        utilisateur = self.get_object(id) 
        serializer = serializers.UtilisateurSerializer(utilisateur)
        if utilisateur:
            return Response({"succes": True, "status": status.HTTP_200_OK, "results": serializer.data}, status=status.HTTP_200_OK)
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "L'utilisateur ayant l'id = {0} n'existe pas !".format(id), }, status=status.HTTP_404_NOT_FOUND,)

    def put(self, request,id=None):
        utilisateur = self.get_object(id)
        if utilisateur:
            serializer = serializers.UtilisateurSerializer(utilisateur, data=request.data)
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


class MedicamentViewSet(viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]
    def list(self, request):
        medicaments = models.Medicament.objects.all()
        page = self.paginate_queryset(medicaments)
        serializer = serializers.MedicamentSerialisers(page, many=True)
        return self.get_paginated_response(serializer.data)


    def post(self,request, *args, **kwarg):
        serializer = serializers.MedicamentSerialisers(data=request.data)
        if serializer.is_valid():
            serializer.save(image=request.FILES.get('image'))
            return Response({'success': True, 'status': status.HTTP_201_CREATED, 'message': 'Medicament crée avec succès', 'results':serializer.data}, status = status.HTTP_201_CREATED)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, 'message': "Erreur de création d'un médicament. Paramètres incomplèts !", 'results': serializer.errors} ,status=status.HTTP_400_BAD_REQUEST)


class MedicamentDetailViewSet(viewsets.ViewSet):
    def get_object(self, id):
        try:
            return models.Medicament.objects.get(id=id)
        except models.Medicament.DoesNotExist:
            return False

    def retrieve(self,request,id=None):
        medicament = self.get_object(id) 
        serializer = serializers.MedicamentSerialisers(medicament) 
        if medicament:
            return Response({"succes": True, "status": status.HTTP_200_OK, "message": "Médicament trouvé" ,"results": serializer.data}, status=status.HTTP_200_OK)
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "Le medicament ayant l'id = {0} n'existe pas !".format(id),}, status=status.HTTP_404_NOT_FOUND,)

    def put(self, request,id=None):
        medicament = self.get_object(id)
        if medicament:
            serializer = serializers.MedicamentSerialisers(medicament, data=request.data)
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
        medicaments = models.Medicament.objects.filter(pharmacie__id=int(idPharmacie))
        Serializer = serializers.MedicamentSerialisers(medicaments, many=True)
        return Response({'status': status.HTTP_200_OK,'success': True,'message': "liste des médicaments d'une pharmacie",'results': Serializer.data,},status=status.HTTP_200_OK,)

class ListCategorieForMedicament(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def list(self, request, idCategorie=None, *args, **kwargs):
        listCategorie = models.Medicament.objects.filter(categorie__id=idCategorie)
        Serializer = serializers.MedicamentSerialisers(listCategorie, many=True)
        return Response({ 'status': status.HTTP_200_OK, 'success': True, 'message': "Liste des medicaments d'une Categorie  ", 'results': Serializer.data,},status=status.HTTP_200_OK,)

class SymptomeViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]

    def list(self, request, *args, **kwargs):
        symptome = models.Symptome.objects.all()
        serializer = models.SymptomeSerializers(symptome, many=True)
        return Response({'status': status.HTTP_200_OK,'success': True,'message': 'Liste des symptomes', 'results':serializer.data},status=status.HTTP_200_OK,)

    def post(self, request, *args, **kwargs):
        
        serializer = serializers.SymptomeSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_200_OK, 'message': 'Sypmtome crée avec succès', 'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({ 'success': False, 'status': status.HTTP_400_BAD_REQUEST, 'message': 'Paramètre de création imcomplèts',  'results': serializer.errors, }, status=status.HTTP_400_BAD_REQUEST)


class SymptomeDetailViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    def get_object(self,id):
        try:
            return models.Symptome.objects.get(id=id)
        except models.Symptome.DoesNotExist:
                return False  
                 
    def retrieve(self, request, id=None,):
        symptome = self.get_object(id)
        if symptome:
            serializer = serializers.SymptomeSerializers(symptome)
            return Response({"succes": True, "status": status.HTTP_200_OK, 'message': 'Symptôme trouvé', "results": serializer.data}, status=status.HTTP_200_OK)
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "Le symptome ayant l'id = {0} n'existe pas !".format(id), }, status=status.HTTP_404_NOT_FOUND,)
    
    def put(self,request,id=None):
        symptome = self.get_object(id)
        
        if symptome:
            serializer = serializers.SymptomeSerializers(symptome, data=request.data)
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
       
        consultation = models.objectsConsultaion.objects.all()
        serializer = serializers.ConsultationSerializers(consultation, many=True)
        return Response({'status': status.HTTP_200_OK,'success': True,'message': 'Liste des consultations', 'results':serializer.data},status=status.HTTP_200_OK,)

    def post(self, request, *args, **kwargs):
        
        serializer = serializers.ConsultationSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_200_OK, 'message': 'Consultation crée avec succès', 'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({ 'success': False, 'message' : 'Erreur de création ! Paramètres incomplèts','status': status.HTTP_400_BAD_REQUEST, 'results': serializer.errors }, status=status.HTTP_400_BAD_REQUEST) 


class ConsultationDetailViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    def get_object(self,id):
        try:
            return models.Consultaion.objects.get(id=id)
        except models.Consultaion.DoesNotExist:
                return False  
                 
    def retrieve(self, request, id=None,):
        consultation = self.get_object(id)
        if consultation:
            serializer = serializers.ConsultationSerializers(consultation)
            return Response({"succes": True, "status": status.HTTP_200_OK, 'message': "Consultation trouvée", "results": serializer.data}, status=status.HTTP_200_OK)
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "La consultation ayant l'id = {0} n'existe pas !".format(id), }, status=status.HTTP_404_NOT_FOUND,)
    
    def put(self,request,id=None):
        consultation = self.get_object(id)
        
        if consultation:
            serializer = serializers.ConsultationSerializers(consultation, data=request.data)
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
        listConsultation = models.Consultaion.objects.filter(user=request.user.id)
        Serializer = serializers.ConsultationSerializers(listConsultation, many=True)
        return Response({'status': status.HTTP_200_OK,'success': True,'message': "Liste des consultations d'un utilisateur",'results': Serializer.data,},status=status.HTTP_200_OK,)    

class MaladieViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    def list(self, request, *args, **kwargs):
        maladie = models.Maladie.objects.all()
        serializer = serializers.MaladieSerializers(maladie, many=True)
        return Response({'status': status.HTTP_200_OK,'success': True,'message': 'Liste des maladies', 'results':serializer.data},status=status.HTTP_200_OK,)

    def post(self, request, *args, **kwargs):
        serializer = serializers.MaladieSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_200_OK, 'message': 'Maladie enregistrée avec succès', 'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({ 'success': False, 'status': status.HTTP_400_BAD_REQUEST, 'message' : 'Erreur de création ! Paramètres incomplèts', 'results': serializer.errors }, status=status.HTTP_400_BAD_REQUEST)


class MaladieDetailViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    def get_object(self,id):
        try:
            return models.Maladie.objects.get(id=id)
        except models.Maladie.DoesNotExist:
                return False  
                 
    def retrieve(self, request, id=None,):
        maladie = self.get_object(id)
        if maladie:
            serializer = serializers.MaladieSerializers(maladie)
            return Response({"succes": True, "status": status.HTTP_200_OK, 'message': 'Maladie trouvée', "results": serializer.data}, status=status.HTTP_200_OK)
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "La maladie ayant l'id = {0} n'existe pas !".format(id), }, status=status.HTTP_404_NOT_FOUND,)
    
    def put(self,request,id=None):
        maladie = self.get_object(id)
        if maladie:
            serializer = serializers.MaladieSerializers(maladie, data=request.data)
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

class FilterMedicamentViewSet(viewsets.GenericViewSet):

    def list(self, request, *args, **kwargs):
        query = request.data.get('query')
        medicaments = models.Medicament.objects.all()
        for dic in query:
            key = list(dic.keys())[0]
            if key == "categorie":
                medicaments = medicaments.filter(categorie__libelle__icontains = dic[key])
            
            if key == "search":
                medicaments = medicaments.filter( 
                Q(nom__icontains = dic[key]) |
                Q(marque__icontains = dic[key]) |
                Q(description__icontains = dic[key]) |
                Q(categorie__libelle__icontains = dic[key]))
                
            if key == "voix":
                medicaments = medicaments.filter(voix__in = dic[key])

        page = self.paginate_queryset(medicaments)
        serializer = serializers.MedicamentSerialisers(page, many=True)
        return self.get_paginated_response(serializer.data)
        

class DetailMedicamentViewset(viewsets.ViewSet):
    
    def get_object(self, id):
        try:
            return models.Medicament.objects.get(id = id)
        except models.Medicament.DoesNotExist:
            return False

    def retrieve(self, request, id=None, *args, **kw): 
        
        medicament = self.get_object(id)
        if medicament:
            serializer = serializers.MedicamentDetailSerialisers(medicament)
            data = serializer.data
            return Response({'success': True, 'status': status.HTTP_200_OK, "message": "Détail du medicament", 'results': data })
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "Le medicament ayant l'id = {0} n'existe pas !".format(id)}, status=status.HTTP_404_NOT_FOUND)    



class CarnetViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    def list(self, request, *args, **kwargs):
        carnet = models.Carnet.objects.all()
        serializer = serializers.CarnetSerializers(carnet, many=True)
        return Response({'status': status.HTTP_200_OK,'success': True,'message': 'Liste des maladies', 'results':serializer.data},status=status.HTTP_200_OK,)

    def post(self, request, *args, **kwargs):
        serializer = serializers.CarnetSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_200_OK, 'message': 'Carnet crée avec succès', 'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'success': False, 'message':'Erreur de création ! Paramètres incomplèts', 'results': serializer.errors }, status=status.HTTP_400_BAD_REQUEST)

class  CarnetDetailViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    def get_object(self,id):
        try:
            return models.Carnet.objects.get(id=id)
        except models.Carnet.DoesNotExist:
                return False  
                 
    def retrieve(self, request, id=None,):
        carnet = self.get_object(id)
        if carnet:
            serializer = serializers.CarnetSerializers(carnet)
            return Response({"succes": True, "status": status.HTTP_200_OK, 'message': 'Cartnet trouvé', "results": serializer.data}, status=status.HTTP_200_OK)
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "La carnet ayant l'id = {0} n'existe pas !".format(id), }, status=status.HTTP_404_NOT_FOUND,)
    
    def put(self,request,id=None):
        carnet = self.get_object(id)
        
        if carnet:
            serializer = serializers.CarnetSerializers(carnet, data=request.data)
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
        carnet = models.Carnet.objects.filter(user=request.user.id)
        serializer = serializers.CarnetSerializers(carnet, many=True)
        return Response({'status': status.HTTP_200_OK,'success': True,'message': "Carnet d'un utilisateur",'results': serializer.data,},status=status.HTTP_200_OK,)