from django.urls import path
from .views import TopManageurAdd, GetAllTopManageurs, GestionTopManageur
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', TopManageurAdd.as_view()),
    path('all', GetAllTopManageurs.as_view()),
    path('<int:id>', GestionTopManageur.as_view()),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)