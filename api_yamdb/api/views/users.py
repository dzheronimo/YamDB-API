from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.permissions import AdminOnly
from api.serializers.users import (CustomJWTSerializer, SignupSerializer,
                                   UserSerializer)
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User


class SignupView(views.APIView):
    """Регистрация пользователя."""
    permission_classes = (permissions.AllowAny, )

    def code_generator(self, user):
        confirmation_code = default_token_generator.make_token(user=user)
        return {'user': user,
                'confirmation_code': confirmation_code}

    def send_verification_code(self, generator):
        mail.send_mail(
            subject='Подтверждение регистрации на YaMDb.ru',
            message=f'Для подверждения регистрации'
            f'воспользуйтесь кодом подверждения \n'
            f'{generator["confirmation_code"]}',
            from_email='no_reply@yamdb.ru',
            recipient_list=[generator['user'].email])

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        self.send_verification_code(self.code_generator(user))
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class CustomJWT(views.APIView):
    """Работа с Токеном."""
    permission_classes = (permissions.AllowAny, )

    def post(self, request):
        serializer = CustomJWTSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(
                user=user, token=confirmation_code):
            payload = {'confirmation_code': 'Ключ не верный'}
            return Response(payload, status=status.HTTP_400_BAD_REQUEST)
        token = str(RefreshToken.for_user(user).access_token)
        payload = {'token': token}
        return Response(payload, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """Ресурс users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly, )
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = [
        method for method in viewsets.ModelViewSet.http_method_names
        if method not in ['put']]

    @action(methods=['get', 'patch'],
            detail=False, url_path='me',
            url_name='get_self_profile',
            permission_classes=(permissions.IsAuthenticated,))
    def get_self_profile(self, request):
        serializer = UserSerializer(
            request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if request.method == 'PATCH':
            serializer.save(role=self.request.user.role)
        return Response(serializer.data, status.HTTP_200_OK)
