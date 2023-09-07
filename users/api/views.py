from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from django.db.models import Max

from users.models import CompletedQuiz
from .serializers import (UserTokenObtainPairSerializer,
                          RegisterSerializer,
                          CompletedQuizSerializer,
                          UserQuizCompletionsSerializer)


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer


class RegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class ListCreateComletedQuizAPIView(ListCreateAPIView):
    queryset = CompletedQuiz.objects.all()
    model = CompletedQuiz

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CompletedQuizSerializer
        if self.request.method == 'GET':
            return UserQuizCompletionsSerializer

    def get_queryset(self):
        user = self.request.user
        if not user.is_staff:
            return CompletedQuiz.objects.filter(user=user).values('quiz', 'quiz__title').annotate(best_score=Max('score'))
        else:
            return CompletedQuiz.objects.all().values('quiz').annotate(best_score=Max('score'))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
