from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserTokenObtainPairView, RegisterAPIView

urlpatterns = [
    path('token/login/', UserTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/register/', RegisterAPIView.as_view(), name='token_create'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
