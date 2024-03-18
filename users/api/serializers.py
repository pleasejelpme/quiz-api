from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from users.models import CompletedQuiz


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token


class RegisterSerializer(serializers.ModelSerializer):
    tokens = serializers.SerializerMethodField()

    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Username already in use. Try another one'
        )]
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password2',
            'tokens'
        ]

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password': 'Password arent the same'})

        return data

    def get_tokens(self, user):
        tokens = RefreshToken.for_user(user)
        refresh = str(tokens)
        access = str(tokens.access_token)
        data = {
            'access': access,
            'refresh': refresh
        }
        return data

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user


# After creating an account, the user can set an email to reset his password if needed.
class SetUserEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(required=True)


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def validate(self, data):
        if data['new_password'] != data['new_password2']:
            raise serializers.ValidationError({
                'password': 'Password arent the same'
            })

        if data['old_password'] == data['new_password'] or data['old_password'] == data['new_password2']:
            raise serializers.ValidationError({
                'password': 'Old and new password cannot be the same'
            })

        return data


# Serializer used to handle creation of completed quizes
class AddCompletedQuizSerializer(serializers.Serializer):
    quiz = serializers.IntegerField()
    score = serializers.IntegerField()


# Serializer that returns the best scores of every quiz an user has completed
class UserQuizCompletionsSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField(source='quiz')
    quiz_title = serializers.CharField(source='quiz__title')
    best_score = serializers.IntegerField()
    completions = serializers.IntegerField(source='times_completed')
