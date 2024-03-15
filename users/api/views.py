from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import CreateAPIView, ListCreateAPIView, UpdateAPIView, GenericAPIView
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
                          UserQuizCompletionsSerializer,
                          SetUserEmailSerializer)


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer


class RegisterAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class SetRecoveryEmailAPIView(UpdateAPIView):
    serializer_class = SetUserEmailSerializer
    model = User

    def get_object(self):
        user = self.request.user
        print(f'The logged user is: {user}')
        return user

    def update(self, request, *args, **kwargs):
        self.user = self.get_object()
        print(self.user)
        serializer = self.get_serializer(data=request.data)

        if self.user.email:
            return Response({'error': 'There is an existing email'}, status=status.HTTP_409_CONFLICT)

        if serializer.is_valid():
            if not self.user.check_password(serializer.data.get('password')):
                return Response({'error': 'wrong password!'}, status=status.HTTP_400_BAD_REQUEST)

            email = serializer.data.get('email')
            print(email)
            self.user.email = email
            self.user.save()
            return Response({'success': 'Email added succesfully!'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        print(request.data)
        self.user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.user.check_password(serializer.data.get('password')):
                return Response({'error': 'wrong password!'}, status=status.HTTP_400_BAD_REQUEST)

            email = serializer.data.get('email')
            self.user.email = email
            self.user.save()
            return Response({'success': 'Email changed successfully!'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class ListCreateComletedQuizAPIView(GenericAPIView):
    model = CompletedQuiz

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CompletedQuizSerializer
        if self.request.method == 'GET':
            return UserQuizCompletionsSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            completions = CompletedQuiz.objects.all().values(
                'quiz', 'quiz__title').annotate(best_score=Max('max_score'))
            return completions

        completions = CompletedQuiz.objects.filter(user=user).values(
            'quiz', 'quiz__title').annotate(best_score=Max('max_score'))
        return completions

    def get(self, request, *args, **kwargs):
        completions = self.get_queryset()
        return Response(completions)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            try:
                quiz_completion = CompletedQuiz.objects.get(
                    quiz=serializer.data.get('quiz'))
                current_max_score = quiz_completion.max_score

                if current_max_score < serializer.data.get('score'):
                    quiz_completion.max_score = serializer.data.get('score')
                    quiz_completion.save()

                quiz_completion.times_completed += 1
                quiz_completion.save()
                return Response({'success': 'completion added'}, status=status.HTTP_204_NO_CONTENT)
            except:
                return Response({'error': 'Quiz not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
