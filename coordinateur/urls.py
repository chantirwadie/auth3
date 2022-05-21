from django.urls import path
from .views import CoordinateurAdd, GetAllCoordinateur, GestionCoordinateur


urlpatterns = [
    path('', CoordinateurAdd.as_view()),
    path('all', GetAllCoordinateur.as_view()),
    path('<int:id>', GestionCoordinateur.as_view()),
]
