from django.urls import path
from .views import RegisterApiView, LoginAPIView, UserApiView, RefreshApiView, LogoutApiView, ForgetPasswordApiView, ResetPasswordApiView

from .views import GeneralStatApiView
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('register', RegisterApiView.as_view()),
    path('login', LoginAPIView.as_view()),
    path('user', UserApiView.as_view()),
    path('refresh', RefreshApiView.as_view()),
    path('logout', LogoutApiView.as_view()),
    path('forgetPassword', ForgetPasswordApiView.as_view()),
    path('resetPassword', ResetPasswordApiView.as_view()),

    path('users/stats', GeneralStatApiView.as_view()),
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
