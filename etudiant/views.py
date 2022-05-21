from .models import Etudiant
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .serializers import EtudiantSerializer, Etudiants
import traceback
from django.http import JsonResponse
from core.models import User
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from django.db.models import CharField
from django.db.models import  Q


# Create your views here.


class EtudiantAdd(APIView):
    """ This class will handle the add of a new etudiant """
    def post(self, request):
        serializer = EtudiantSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class GestionEtudiant(APIView):
    """ This class will handle the CRUD OPERATIONS EXCEPT ADD"""
    def get(self, request, id):
        etudiant = Etudiant.objects.filter(pk=id).first()
        if etudiant:
            serializer = Etudiants(etudiant)
            return Response(serializer.data)
        return Response({"message" : "Ancun étudiant existe avec l'identifiant donné","erreur":"true"}, 400)

    def put(self,request, id):
        etudiantObject = Etudiant.objects.filter(pk=id).first()
        serializer = EtudiantSerializer().update(etudiantObject, request.data)
        
        return Response(EtudiantSerializer(serializer).data, 200)
       
    def delete(self, request, id):
        try:
            etudiantObject = Etudiant.objects.filter(pk=id).first()
            User.objects.filter(pk=etudiantObject.user.id).delete()
            return Response({"message" : "Deleted successfully"})
        except Exception as e:
            m = traceback.format_exc()    
            return Response({"message" : m}, 404)            



class GetAllEtudiants(APIView, PageNumberPagination):

    # queryset = Etudiant.objects.all()
    # serializer_class = Etudiants
    # pagination_class = LimitOffsetPagination
    page_size = 1000
    page_size_query_param = 'page_size'
    page_number = 1
    page_number_query_param = "page"

   
    ETUDIANT_DEFAULT_PAGE_SIZE = 10

    def get_queryset(self):
        
        etudiants = Etudiant.objects.all().order_by('id')
        query = self.request.GET.get('query', None)
        if query:
            fields = [f for f in Etudiant._meta.fields if isinstance(f, CharField)]
            fieldsUser = [f for f in User._meta.fields if isinstance(f, CharField)]
            queries = [Q(**{f.name + "__icontains" : query}) for f in fields]
            queriesUser = [Q(**{f.name + "__icontains" : query}) for f in fieldsUser]
            qs = Q()
            qsUser = Q()
            for query in queries:
                qs = qs | query
            for query in queriesUser:
                qsUser = qsUser | query
            etudiants = etudiants.filter(qs)  
            users = User.objects.filter(qsUser)
            etudiants2 = Etudiant.objects.filter(user__in=users)
            etudiants = etudiants | etudiants2

        etudiants = Etudiants(etudiants, many=True)    


        return self.paginate_queryset(etudiants.data, self.request)

        # raise APIException400(request, {'details': "Bad Request"})

    def get(self, request):
        etudiants = self.get_queryset()
        return self.get_paginated_response({"etudiants": etudiants})

    def post(self, request):

        ids = request.data.get('ids', None)

        if ids:
            User.objects.filter(id__in=ids).delete()
            delete_count = len(ids)
            return Response({"message" : "%d etudiants supprimés avec succès" % delete_count})

        return Response({"message" : "Veuillez fournir un identifiant"}, 400)        
