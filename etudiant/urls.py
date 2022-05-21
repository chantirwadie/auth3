from django.urls import path
from .views import EtudiantAdd, GetAllEtudiants, GestionEtudiant
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', EtudiantAdd.as_view()),
    path('all', GetAllEtudiants.as_view()),
    path('<int:id>', GestionEtudiant.as_view())
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)