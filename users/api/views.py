from base64 import urlsafe_b64encode

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import CreateAPIView, UpdateAPIView, GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.db.models import Max
from django.urls import reverse
from django.utils.encoding import force_bytes

from users.models import CompletedQuiz
from quizes.models import Quiz
from .serializers import (UserTokenObtainPairSerializer,
                          RegisterSerializer,
                          ChangePasswordSerializer,
                          AddCompletedQuizSerializer,
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
        return user

    def update(self, request, *args, **kwargs):
        self.user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if self.user.email:
            return Response({'error': 'There is an existing email'}, status=status.HTTP_409_CONFLICT)

        if serializer.is_valid():
            if not self.user.check_password(serializer.data.get('password')):
                return Response({'error': 'wrong password!'}, status=status.HTTP_400_BAD_REQUEST)

            email = serializer.data.get('email')

            if self.user.email == email:
                return Response(
                    {'error': 'this is your current email, try a new one'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            self.user.email = email
            self.user.save()
            return Response(
                {
                    'success': 'Email added succesfully!',
                    'email': email
                }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        self.user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.user.check_password(serializer.data.get('password')):
                return Response({'error': 'wrong password!'}, status=status.HTTP_400_BAD_REQUEST)

            email = serializer.data.get('email')

            if self.user.email == email:
                return Response(
                    {'error': 'this is your current email, try a new one'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            self.user.email = email
            self.user.save()
            return Response(
                {
                    'success': 'Email changed successfully!',
                    'email': email
                }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    model = User

    def get_object(self):
        user = self.request.user
        return user

    def patch(self, request, *args, **kwargs):
        self.user = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # checks the old password
            if not self.user.check_password(serializer.data.get('old_password')):
                return Response({'error': 'wrong password'}, status=status.HTTP_400_BAD_REQUEST)

            # set the new password
            self.user.set_password(serializer.data.get('new_password'))
            self.user.save()
            return Response({'success': 'Password updated successfully!'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListCreateComletedQuizAPIView(GenericAPIView):
    model = CompletedQuiz

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCompletedQuizSerializer
        if self.request.method == 'GET':
            return UserQuizCompletionsSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            completions = CompletedQuiz.objects.all().values(
                'quiz',
                'quiz__title',
                'times_completed').annotate(best_score=Max('max_score'))
            return completions

        completions = CompletedQuiz.objects.filter(user=user).values(
            'quiz',
            'quiz__title',
            'times_completed').annotate(best_score=Max('max_score'))
        return completions

    def get(self, request, *args, **kwargs):
        serializer = UserQuizCompletionsSerializer
        try:
            completions = self.get_queryset()
            completions = serializer(completions, many=True)
            return Response(completions.data, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            quiz_completion = CompletedQuiz.objects.filter(
                quiz=serializer.data.get('quiz')).first()

            # If the user already completed this quiz, then we check if the new score is better than
            # the max score, if it is then we update the max score, and finally we increment the total completions
            # of this quiz by 1
            if quiz_completion:
                current_max_score = quiz_completion.max_score

                if current_max_score < serializer.data.get('score'):
                    quiz_completion.max_score = serializer.data.get('score')
                    quiz_completion.save()

                quiz_completion.times_completed += 1
                quiz_completion.save()
                return Response({'success': 'completion added'}, status=status.HTTP_204_NO_CONTENT)

            # If there is no completions of this quiz then we proceed to create a new one
            else:
                new_completed_quiz = CompletedQuiz.objects.create(
                    user=self.request.user,
                    quiz=Quiz.objects.get(id=serializer.data.get('quiz')),
                    max_score=serializer.data.get('score')
                )
                new_completed_quiz.save()
                return Response({'success': 'completion added'}, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
