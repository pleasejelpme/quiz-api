from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User

from users.models import CompletedQuiz
from .serializers import UserTokenObtainPairSerializer, RegisterSerializer, CompletedQuizSerializer


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer


class RegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class ListCreateComletedQuizAPIView(ListCreateAPIView):
    queryset = CompletedQuiz.objects.all()
    serializer_class = CompletedQuizSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
