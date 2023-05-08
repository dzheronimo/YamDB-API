from django.conf import settings
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import IntegrityError
from rest_framework import serializers

from api.validators import CorrectUsernameValidator
from users.models import User


class SignupSerializer(serializers.Serializer):
    """Регистрация пользователя."""
    email = serializers.EmailField(max_length=settings.LENGTH_EMAIL)
    username = serializers.CharField(max_length=settings.LENGTH_USERNAME,
                                     validators=[UnicodeUsernameValidator(),
                                                 CorrectUsernameValidator()])

    def create(self, validated_data):
        try:
            user, created = User.objects.get_or_create(
                username=validated_data.get('username'),
                email=validated_data.get('email')
            )
        except IntegrityError:
            raise serializers.ValidationError(
                'Пользователь с такими данными уже существует')
        return user


class UserSerializer(serializers.ModelSerializer):
    """Ресурс users."""
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


class CustomJWTSerializer(serializers.Serializer):
    """Работа с Токеном."""
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)
