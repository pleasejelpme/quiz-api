from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from users.models import CompletedQuiz


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Username already in use, try another one'
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
            'password2'
        ]

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'error': 'Password arent the same'})
        return data

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class CompletedQuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompletedQuiz
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}
        }
