from django.http import JsonResponse
from rest_framework.views import APIView
from .serializers import ProfesseurSerializer, Professeurs
from core.serializers import UserSerializer
from .models import Professeur
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.pagination import PageNumberPagination
from django.db.models import CharField
from django.db.models import  Q
from django.db.models import Prefetch

import traceback
from core.models import User
import urllib3
import json



http = urllib3.PoolManager()

class ProfesseurAdd(APIView):
    """ This class will handle the add of a new professeur """
    # permission_classes [permessions.IsAuthenticated]
    parser_class = [MultiPartParser,FormParser]
    def post(self, request,format=None):
        serializer = ProfesseurSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get(self, request):
        serializer = Professeurs(Professeur.objects.all(), many=True)
        return Response(serializer.data)

         


class GestionProfesseur(APIView):
    parser_class = [MultiPartParser,FormParser]
    """ This class will handle the CRUD OPERATIONS EXCEPT ADD"""
    def get(self, request, id):
        professeur = Professeur.objects.filter(pk=id).first()
        if professeur:
            serializer = Professeurs(professeur)
            idDepartement = serializer.data['departement']
            url = 'http://localhost:8000/api/v2/departement' 
            final_url = '/'.join([url, str(idDepartement)])
            r = http.request('GET', final_url)
            data = json.loads(r.data)
            serializer.data['departement']=data
            return Response({"professeur": serializer.data,"departement":data})
        return Response({"message" : "Ancun professeur existe avec l'identifiant donné"}, 400)

    def put(self,request, id):
        professeurObject = Professeur.objects.filter(pk=id).first()
        serializer = ProfesseurSerializer().update(professeurObject, request.data)
        
        return Response(ProfesseurSerializer(serializer).data, 200)
       
    def delete(self, request,id):
        try:
            professeurObject = Professeur.objects.filter(pk=id).first()
            User.objects.filter(pk=professeurObject.user.id).delete()
            return Response({"message" : "Deleted successfully"})
        except Exception as e:
            m = traceback.format_exc()    
            return Response({"message" : m}, 404)            
 


class GetAllProfeseurs(APIView, PageNumberPagination):

    page_size = 1000
    page_size_query_param = 'page_size'
    page_number = 1
    page_number_query_param = "page"

    def get_queryset(self):
        # product_sync_ts = self.request.GET.get('product_sync_ts', None)
        # if product_sync_ts:
        #     products = Etudiant.objects.filter(update_ts__gt=product_sync_ts)
        professeurs = Professeur.objects.all().order_by('id')
        query = self.request.GET.get('query', None)
        if query:
            fields = [f for f in Professeur._meta.fields if isinstance(f, CharField)]
            fieldsUser = [f for f in User._meta.fields if isinstance(f, CharField)]
            queries = [Q(**{f.name + "__icontains" : query}) for f in fields]
            queriesUser = [Q(**{f.name + "__icontains" : query}) for f in fieldsUser]
            qs = Q()
            qsUser = Q()
            for query in queries:
                qs = qs | query
            for query in queriesUser:
                qsUser = qsUser | query    
            professeurs = Professeur.objects.filter(qs)
            users = User.objects.filter(qsUser).all().order_by('id')
            professeurs2 = Professeur.objects.filter(user__in=users)
            professeurs  = professeurs2 | professeurs
            
            
        queryset = Professeurs(professeurs, many=True) 
        for i in range(len(queryset.data)):
            idDepartement = queryset.data[i]['departement']
            url = 'http://localhost:8000/api/v2/departement'  # no trailing /
            final_url = '/'.join([url, str(idDepartement)])
            r = http.request('GET', final_url)
            data = json.loads(r.data)
            queryset.data[i]['departement']=data 
        return self.paginate_queryset(queryset.data, self.request)


    def get(self, request):
        professeurs = self.get_queryset()
       
        # page_number = request.GET.get('page', 1)
        # page_obj = paginator.get_page(page_number)
        return self.get_paginated_response({"professeurs": professeurs})

    def post(self, request):

        ids = request.data.get('ids', None)

        if ids:
            User.objects.filter(id__in=ids).delete()
            delete_count = len(ids)
            return Response({"message" : "%d professeurs supprimés avec succès" % delete_count})

        return Response({"message" : "Veuillez fournir un identifiant"}, 400)    

        