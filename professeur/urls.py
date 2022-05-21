from django.urls import path
from .views import ProfesseurAdd, GetAllProfeseurs, GestionProfesseur
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', ProfesseurAdd.as_view()),
    path('all', GetAllProfeseurs.as_view()),
    path('<int:id>', GestionProfesseur.as_view()),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)