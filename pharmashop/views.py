
from math import radians, cos, sin, asin, sqrt

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Carnet, Symptome,Utilisateur,Categorie,\
    Pharmacie,Medicament



# Create your views here.


#☺ Python 3 program to calculate Distance Between Two Points on Earth

def distance(lat1, lat2, lon1, lon2):
     
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
      
    # calculate the result
    return(c * r)
     
     
# driver code
lat1 = 53.32055555555556
lat2 = 53.31861111111111
lon1 = -1.7297222222222221
lon2 =  -1.6997222222222223
print(distance(lat1, lat2, lon1, lon2), "K.M")


from .serializers import PharmacieSerializers,UtilisateurSerializer,\
    CategorieSerializers,MedicamentSerialisers
   


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
        # Utilisateur.objects.create(
        #     password= "john",
        #     username= "john",
        #     email= "john@gmail.com",
        #     is_staff= True,
        #     is_active = True,
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
