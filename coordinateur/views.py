from django.http import JsonResponse
from rest_framework.views import APIView
from .serializers import CoordinateurSerializer, Coordinateurs
from core.serializers import UserSerializer
from .models import Coordinateur
from rest_framework.response import Response
import traceback
from core.models import User
import urllib3
import json
from rest_framework.pagination import PageNumberPagination
from django.db.models import CharField
from django.db.models import  Q



http = urllib3.PoolManager()

class CoordinateurAdd(APIView):
    """ This class will handle the add of a new coordinateur """
    def post(self, request):
        serializer = CoordinateurSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

         


class GestionCoordinateur(APIView):
    """ This class will handle the CRUD OPERATIONS EXCEPT ADD"""
    def get(self, request, id):
        coordinateur = Coordinateur.objects.filter(pk=id).first()
        if coordinateur:
            serializer = Coordinateurs(coordinateur)
            idDepartement = serializer.data['departement']
            url = 'http://localhost:8000/api/v2/departement' 
            final_url = '/'.join([url, str(idDepartement)])
            r = http.request('GET', final_url)
            data = json.loads(r.data)
            serializer.data['departement']=data
            return Response({"coordinateur": serializer.data,"departement":data})
        return Response({"message" : "Ancun professeur existe avec l'identifiant donné"}, 400)

    def put(self,request, id):
        coordinateurObject = Coordinateur.objects.filter(pk=id).first()
        serializer = CoordinateurSerializer().update(coordinateurObject, request.data)
        
        return Response(CoordinateurSerializer(serializer).data, 200)
       
    def delete(self, request,id):
        try:
            coordinateurObject = Coordinateur.objects.filter(pk=id).first()
            User.objects.filter(pk=coordinateurObject.user.id).delete()
            return Response({"message" : "Deleted successfully"})
        except Exception as e:
            m = traceback.format_exc()    
            return Response({"message" : m}, 404)            
 


class GetAllCoordinateur(APIView, PageNumberPagination):

    page_size = 1000
    page_size_query_param = 'page_size'
    page_number = 1
    page_number_query_param = "page"

    def get_queryset(self):
        # product_sync_ts = self.request.GET.get('product_sync_ts', None)
        # if product_sync_ts:
        #     products = Etudiant.objects.filter(update_ts__gt=product_sync_ts)
        coordinateurs  = Coordinateur.objects.all().order_by('id') 
        query = self.request.GET.get('query', None)
        if query:
            fields = [f for f in Coordinateur._meta.fields if isinstance(f, CharField)]
            fieldsUser = [f for f in User._meta.fields if isinstance(f, CharField)]
            queries = [Q(**{f.name + "__icontains" : query}) for f in fields]
            queriesUser = [Q(**{f.name + "__icontains" : query}) for f in fieldsUser]
            qs = Q()
            qsUser = Q()
            for query in queries:
                qs = qs | query
            for query in queriesUser:
                qsUser = qsUser | query    
            coordinateurs = Coordinateur.objects.filter(qs)
            users = User.objects.filter(qsUser).all().order_by('id')
            coordinateurs2 = Coordinateur.objects.filter(user__in=users)
            coordinateurs  = coordinateurs2 | coordinateurs
        queryset = Coordinateurs(coordinateurs, many=True)     

        for i in range(len(queryset.data)):
            idDepartement = queryset.data[i]['departement']
            url = 'http://localhost:8000/api/v2/departement'
            final_url = '/'.join([url, str(idDepartement)])
            r = http.request('GET', final_url)
            data = json.loads(r.data)
            queryset.data[i]['departement']=data 
        return self.paginate_queryset(queryset.data, self.request)

    def get(self, request):
        coordinateurs = self.get_queryset()
        return self.get_paginated_response({"coordinateurs": coordinateurs})

    def post(self, request):

        ids = request.data.get('ids', None)

        if ids:
            User.objects.filter(id__in=ids).delete()
            delete_count = len(ids)
            return Response({"message" : "%d coordinateurs supprimés avec succès" % delete_count})

        return Response({"message" : "Veuillez fournir un identifiant"}, 400)    