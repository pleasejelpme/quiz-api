from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserTokenObtainPairView,
    RegisterAPIView,
    ListCreateComletedQuizAPIView,
    ChangePasswordAPIView,
    SetRecoveryEmailAPIView)

urlpatterns = [
    path('token/login/', UserTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('token/register/', RegisterAPIView.as_view(), name='token_create'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('change-password/', ChangePasswordAPIView.as_view(), name='change_password'),
    path('recover-password/', include('django_rest_passwordreset.urls',
         namespace='recover_password')),

    path('set-email/', SetRecoveryEmailAPIView.as_view(), name='set_email'),

    path('completed-quizes/', ListCreateComletedQuizAPIView.as_view(),
         name='completed-quizes'),

]
