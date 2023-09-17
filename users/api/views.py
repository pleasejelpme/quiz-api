from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import CreateAPIView, ListCreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Max

from users.models import CompletedQuiz
from .serializers import (UserTokenObtainPairSerializer,
                          RegisterSerializer,
                          ChangePasswordSerializer,
                          CompletedQuizSerializer,
                          UserQuizCompletionsSerializer)


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer


class RegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class ChangePasswordAPIView(UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User

    def get_object(self):
        user = self.request.user
        return user

    def update(self, request, *args, **kwargs):
        self.user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # checks the old password
            if not self.user.check_password(serializer.data.get('old_password')):
                return Response({'error': 'wrong password'}, status=status.HTTP_400_BAD_REQUEST)

            # set the new password
            self.user.set_password(serializer.data.get('new_password'))
            self.user.save()
            response = {
                'status': status.HTTP_204_NO_CONTENT,
                'message': 'Password updated successfully!',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            return CompletedQuiz.objects.all().values('quiz', 'quiz__title').annotate(best_score=Max('score'))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
