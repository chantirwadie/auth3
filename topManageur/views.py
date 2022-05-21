from .models import TopManageur
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .serializers import TopManageurSerializer, TopManageurs
import traceback
from django.http import JsonResponse
from core.models import User
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from django.db.models import CharField
from django.db.models import  Q


# Create your views here.


class TopManageurAdd(APIView):
    """ This class will handle the add of a new etudiant """
    def post(self, request):
        serializer = TopManageurSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class GestionTopManageur(APIView):
    """ This class will handle the CRUD OPERATIONS EXCEPT ADD"""
    def get(self, request, id):
        topManageur = TopManageur.objects.filter(pk=id).first()
        if topManageur:
            serializer = TopManageur(topManageur)
            return Response(serializer.data)
        return Response({"message" : "Ancun étudiant existe avec l'identifiant donné","erreur":"true"}, 400)

    def put(self,request, id):
        etudiantObject = TopManageur.objects.filter(pk=id).first()
        serializer = TopManageurSerializer().update(etudiantObject, request.data)
        
        return Response(TopManageurSerializer(serializer).data, 200)
       
    def delete(self, request, id):
        try:
            etudiantObject = TopManageur.objects.filter(pk=id).first()
            User.objects.filter(pk=etudiantObject.user.id).delete()
            return Response({"message" : "Deleted successfully"})
        except Exception as e:
            m = traceback.format_exc()    
            return Response({"message" : m}, 404)            



class GetAllTopManageurs(APIView, PageNumberPagination):

    # queryset = Etudiant.objects.all()
    # serializer_class = Etudiants
    # pagination_class = LimitOffsetPagination
    page_size = 1000
    page_size_query_param = 'page_size'
    page_number = 1
    page_number_query_param = "page"

   
    ETUDIANT_DEFAULT_PAGE_SIZE = 10

    def get_queryset(self):
        # product_sync_ts = self.request.GET.get('product_sync_ts', None)
        # if product_sync_ts:
        #     products = Etudiant.objects.filter(update_ts__gt=product_sync_ts)
        topManageurs = TopManageur.objects.all().order_by('id')
        query = self.request.GET.get('query', None)
        if query:
            fields = [f for f in TopManageur._meta.fields if isinstance(f, CharField)]
            fieldsUser = [f for f in User._meta.fields if isinstance(f, CharField)]
            queries = [Q(**{f.name + "__icontains" : query}) for f in fields]
            queriesUser = [Q(**{f.name + "__icontains" : query}) for f in fieldsUser]
            qs = Q()
            qsUser = Q()
            for query in queries:
                qs = qs | query
            for query in queriesUser:
                qsUser = qsUser | query    
            topManageurs = TopManageur.objects.filter(qs)
            users = User.objects.filter(qsUser).all().order_by('id')
            topManageurs2 = TopManageur.objects.filter(user__in=users)
            topManageurs  = topManageurs2 | topManageurs
        queryset = TopManageurs(topManageurs, many=True) 
        return self.paginate_queryset(queryset.data, self.request)

    def get(self, request):
        topManageurs = self.get_queryset()
        return self.get_paginated_response({"topManageurs": topManageurs})

    def post(self, request):

        ids = request.data.get('ids', None)

        if ids:
            User.objects.filter(id__in=ids).delete()
            delete_count = len(ids)
            return Response({"message" : "%d topManageurs supprimés avec succès" % delete_count})

        return Response({"message" : "Veuillez fournir un identifiant"}, 400)        