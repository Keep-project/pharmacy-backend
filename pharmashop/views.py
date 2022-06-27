


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
    def list(self, request):
        pharmacie = Pharmacie.objects.all()
        Serializer = PharmacieSerializers(pharmacie, many=True)
        return Response({'status': status.HTTP_200_OK,'success': True,'message': 'Liste des pharmacies','results': Serializer.data,},status=status.HTTP_200_OK,)


    def post(self, request, *args, **kwargs):
        serializer = PharmacieSerializers(data=request.data)
        if serializer.is_valid():
                
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_200_OK, 'message': 'pharmacies créée avec succès', 'results': serializer.data}, status=status.HTTP_200_OK)
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
            return Response({'status':status.HTTP_200_OK, 'success': True,'results':serializer.data}, status=status.HTTP_200_OK) 
        return Response({'status': status.HTTP_400_BAD_REQUEST,'success': False, 'message':"La pharmacie ayant l'id={0} n'existe pas !".format(id), })          

    def put(self, request,id=None):
        pharmacie = self.get_object(id)
        if pharmacie:
            serializer = PharmacieSerializers(pharmacie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': status.HTTP_201_CREATED,'success': True, "pharmacie":serializer.data}, status=status.HTTP_200_OK)
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors})
        return Response({'status': status.HTTP_404_NOT_FOUND,"message":"la pharmacie ayant l'id = {0} n'existe pas !".format(id),})        
                            
    def delete(self, request, id=None):
        pharmacie = self.get_object(id)
        if pharmacie:
            pharmacie.delete()
            return Response({'status':status.HTTP_201_CREATED, 'success':True, 'message':"Pharmacie supprimée avec succès"},status=status.HTTP_201_CREATED)
        return Response({'status':status.HTTP_404_NOT_FOUND, "message":"La Pharmacie ayant l'id = {0} n'existe pas !".format(id),})    


class CategorieViewSet(viewsets.ViewSet):

    def list(self, request, *args, **kwargs):
        Utilisateur.objects.create(
            password= "john",
            username= "john1234",
            email= "john@gmail.com",
            is_staff= True,
            is_active = True,
        )
        categorie = Categorie.objects.all()
        serializer = CategorieSerializers(categorie, many=True)
        return Response({'status': status.HTTP_200_OK,'success': True,'message': 'Liste des categorie', 'results':serializer.data},status=status.HTTP_200_OK,)

    def post(self, request, *args, **kwargs):
        
        serializer = CategorieSerializers(data=request.data)
        if serializer.is_valid():
            
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_200_OK, 'message': 'Catégorie crée avec succès', 'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors }, status=status.HTTP_400_BAD_REQUEST)

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
                return Response({'status':status.HTTP_201_CREATED, 'success':True, 'categorie':serializer.data},status=status.HTTP_201_CREATED)
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors}) 
        return Response({'status':status.HTTP_404_NOT_FOUND, "message":"La categorie ayant l'id = {0} n'existe pas !".format(id),})       

    def delete(self, request, id=None):
        categorie = self.get_object(id)
        if categorie:
            categorie.delete()
            return Response({'status':status.HTTP_201_CREATED, 'success':True, 'message':"Categorie supprimée avec succès"},status=status.HTTP_201_CREATED)
        return Response({'status':status.HTTP_404_NOT_FOUND, "message":"La categorie ayant l'id = {0} n'existe pas !".format(id),})       

            
            

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
                serializer.save()
                return Response({'status': status.HTTP_201_CREATED,'success': True, "pharmacie":serializer.data}, status=status.HTTP_200_OK)
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors})
        return Response({'status': status.HTTP_404_NOT_FOUND,"message":"L'utilisateur ayant l'id = {0} n'existe pas !".format(id),})

    def delete(self, request, id=None):
        utilisateur = self.get_object(id)
        if utilisateur:
            utilisateur.delete()
            return Response({'status':status.HTTP_201_CREATED, 'success':True, 'message':"Utilisateur supprimée avec succès"},status=status.HTTP_201_CREATED)
        return Response({'status':status.HTTP_404_NOT_FOUND, "message":"L' utilisateur ayant l'id = {0} n'existe pas !".format(id),})


class MedicamentViewSet(viewsets.ViewSet):
    def list(self, request):
        medicament = Medicament.objects.all()
        serializer = MedicamentSerialisers(medicament, many=True)
        return Response({'success': True, 'status':status.HTTP_200_OK, 'message': 'liste des medicaments','results':serializer.data}, status=status.HTTP_200_OK)


    def post(self,request, *args, **kwarg):
        serializer = MedicamentSerialisers(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_201_CREATED, 'message': 'Medicament crée avec success', 'results':serializer.data}, status = status.HTTP_201_CREATED)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors }, status=status.HTTP_400_BAD_REQUEST)


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
               
            return Response({"succes": True, "status": status.HTTP_200_OK, "results": serializer.data}, status=status.HTTP_200_OK)
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "Le medicament ayant l'id = {0} n'existe pas !".format(id),}, status=status.HTTP_404_NOT_FOUND,)

    def put(self, request,id=None):
        medicament = self.get_object(id)
        if medicament:
            serializer = MedicamentSerialisers(medicament, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': status.HTTP_201_CREATED,'success': True, "pharmacie":serializer.data}, status=status.HTTP_200_OK)
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors})
        return Response({'status': status.HTTP_404_NOT_FOUND,"message":"le medicament ayant l'id = {0} n'existe pas !".format(id),})        

    def delete(self, request, id=None):
        medicament = self.get_object(id)
        if medicament:
            medicament.delete()
            return Response({'status':status.HTTP_201_CREATED, 'success':True, 'message':"Medicament supprimée avec succès"},status=status.HTTP_201_CREATED)
        return Response({'status':status.HTTP_404_NOT_FOUND, "message":"Le medicament ayant l'id = {0} n'existe pas !".format(id),})  




class SymptomeViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    def list(self, request, *args, **kwargs):
        # Utilisateur.objects.create(
        #     password= "john",
        #     username= "john",
        #     email= "john@gmail.com",
        #     is_staff= True,
        #     is_active = True,
        # )
        symptome = Symptome.objects.all()
        serializer = SymptomeSerializers(symptome, many=True)
        return Response({'status': status.HTTP_200_OK,'success': True,'message': 'Liste des symptomes', 'results':serializer.data},status=status.HTTP_200_OK,)

    def post(self, request, *args, **kwargs):
        
        serializer = SymptomeSerializers(data=request.data)
        if serializer.is_valid():
            
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_200_OK, 'message': 'Sypmtome crée avec succès', 'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors }, status=status.HTTP_400_BAD_REQUEST)


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
            
            return Response({"succes": True, "status": status.HTTP_200_OK, "results": serializer.data}, status=status.HTTP_200_OK)
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "Le symptome ayant l'id = {0} n'existe pas !".format(id), }, status=status.HTTP_404_NOT_FOUND,)
    
    def put(self,request,id=None):
        symptome = self.get_object(id)
        
        if symptome:
            serializer = SymptomeSerializers(symptome, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':status.HTTP_201_CREATED, 'success':True, 'sypmtome':serializer.data},status=status.HTTP_201_CREATED)
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors}) 
        return Response({'status':status.HTTP_404_NOT_FOUND, "message":"Le symptome ayant l'id = {0} n'existe pas !".format(id),})       

    def delete(self, request, id=None):
        categorie = self.get_object(id)
        if categorie:
            categorie.delete()
            return Response({'status':status.HTTP_201_CREATED, 'success':True, 'message':"symptome supprimée avec succès"},status=status.HTTP_201_CREATED)
        return Response({'status':status.HTTP_404_NOT_FOUND, "message":"Le symptome ayant l'id = {0} n'existe pas !".format(id),}) 



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
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors }, status=status.HTTP_400_BAD_REQUEST) 


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
            
            return Response({"succes": True, "status": status.HTTP_200_OK, "results": serializer.data}, status=status.HTTP_200_OK)
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "La consultation ayant l'id = {0} n'existe pas !".format(id), }, status=status.HTTP_404_NOT_FOUND,)
    
    def put(self,request,id=None):
        consultation = self.get_object(id)
        
        if consultation:
            serializer = ConsultationSerializers(consultation, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':status.HTTP_201_CREATED, 'success':True, 'consultation':serializer.data},status=status.HTTP_201_CREATED)
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors}) 
        return Response({'status':status.HTTP_404_NOT_FOUND, "message":"La consultation ayant l'id = {0} n'existe pas !".format(id),})       

    def delete(self, request, id=None):
        consultation = self.get_object(id)
        if consultation:
            consultation.delete()
            return Response({'status':status.HTTP_201_CREATED, 'success':True, 'message':"consultation supprimée avec succès"},status=status.HTTP_201_CREATED)
        return Response({'status':status.HTTP_404_NOT_FOUND, "message":"La consultation ayant l'id = {0} n'existe pas !".format(id),})                           

        

class MaladieViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    def list(self, request, *args, **kwargs):
       
        maladie = Maladie.objects.all()
        serializer = MaladieSerializers(maladie, many=True)
        return Response({'status': status.HTTP_200_OK,'success': True,'message': 'Liste des maladies', 'results':serializer.data},status=status.HTTP_200_OK,)

    def post(self, request, *args, **kwargs):
        data =  request.data
      
        serializer = MaladieSerializers(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_200_OK, 'message': 'Maladie crée avec succès', 'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors }, status=status.HTTP_400_BAD_REQUEST)


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
            
            return Response({"succes": True, "status": status.HTTP_200_OK, "results": serializer.data}, status=status.HTTP_200_OK)
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "La maladie ayant l'id = {0} n'existe pas !".format(id), }, status=status.HTTP_404_NOT_FOUND,)
    
    def put(self,request,id=None):
        maladie = self.get_object(id)
        
        if maladie:
            serializer = MaladieSerializers(maladie, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':status.HTTP_201_CREATED, 'success':True, 'maladie':serializer.data},status=status.HTTP_201_CREATED)
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors}) 
        return Response({'status':status.HTTP_404_NOT_FOUND, "message":"La maladie ayant l'id = {0} n'existe pas !".format(id),})       

    def delete(self, request, id=None):
        maladie = self.get_object(id)
        if maladie:
            maladie.delete()
            return Response({'status':status.HTTP_201_CREATED, 'success':True, 'message':"consultation supprimée avec succès"},status=status.HTTP_201_CREATED)
        return Response({'status':status.HTTP_404_NOT_FOUND, "message":"La consultation ayant l'id = {0} n'existe pas !".format(id),})                           


        
class CarnetViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    def list(self, request, *args, **kwargs):
       
        carnet = Carnet.objects.all()
        serializer = MaladieSerializers(carnet, many=True)
        return Response({'status': status.HTTP_200_OK,'success': True,'message': 'Liste des maladies', 'results':serializer.data},status=status.HTTP_200_OK,)

    def post(self, request, *args, **kwargs):
        serializer = CarnetSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': True, 'status': status.HTTP_200_OK, 'message': 'Carnet crée avec succès', 'results': serializer.data}, status=status.HTTP_200_OK)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors }, status=status.HTTP_400_BAD_REQUEST)



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
            
            return Response({"succes": True, "status": status.HTTP_200_OK, "results": serializer.data}, status=status.HTTP_200_OK)
        return Response({"succes": False, "status": status.HTTP_404_NOT_FOUND, "message": "La carnet ayant l'id = {0} n'existe pas !".format(id), }, status=status.HTTP_404_NOT_FOUND,)
    
    def put(self,request,id=None):
        carnet = self.get_object(id)
        
        if carnet:
            serializer = CarnetSerializers(carnet, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'status':status.HTTP_201_CREATED, 'success':True, 'carnet':serializer.data},status=status.HTTP_201_CREATED)
            return Response({'status': status.HTTP_400_BAD_REQUEST, 'data': serializer.errors}) 
        return Response({'status':status.HTTP_404_NOT_FOUND, "message":"Le carnet ayant l'id = {0} n'existe pas !".format(id),})       

    def delete(self, request, id=None):
        maladie = self.get_object(id)
        if maladie:
            maladie.delete()
            return Response({'status':status.HTTP_201_CREATED, 'success':True, 'message':"Carnet supprimée avec succès"},status=status.HTTP_201_CREATED)
        return Response({'status':status.HTTP_404_NOT_FOUND, "message":"La carnet ayant l'id = {0} n'existe pas !".format(id),})                           

