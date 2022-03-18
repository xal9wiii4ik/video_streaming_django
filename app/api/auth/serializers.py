import typing as tp

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model, password_validation

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from base import settings


class RegisterUserSerializer(serializers.Serializer):
    """
    Serializer for register new user
    """

    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=500, required=True)
    repeat_password = serializers.CharField(max_length=500, required=True)
    email = serializers.CharField(max_length=100, required=False)
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)

    @staticmethod
    def validate_username(username: str) -> str:
        try:
            get_user_model().objects.get(username=username)
            raise serializers.ValidationError({'User with this username already exist'})
        except ObjectDoesNotExist:
            return username

    @staticmethod
    def validate_email(email: str) -> str:
        try:
            get_user_model().objects.get(email=email)
            raise serializers.ValidationError({'User with this email already exist'})
        except ObjectDoesNotExist:
            return email

    @staticmethod
    def validate_password(password: str) -> str:
        # django will raise exception if bad value
        password_validation.validate_password(password=password)
        return password

    def validate(self, attrs: tp.Dict[str, tp.Any]) -> tp.Dict[str, tp.Any]:
        """
        Validate all fields
        Args:
            attrs: OrderedDict with values
        Raise:
            exception if invalid fields
        Returns:
            attrs
        """

        if attrs.get('password') != attrs.get('repeat_password'):
            raise serializers.ValidationError({'repeat_password': 'Repeat password should be equal to password'})
        attrs['password'] = make_password(password=attrs['password'])
        return attrs


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """ Custom token serializer """

    def validate(self, attrs: tp.Dict[str, tp.Any]) -> tp.Dict[str, tp.Any]:
        """ add fields to response data """

        data: tp.Dict[str, tp.Any] = super(CustomTokenObtainPairSerializer, self).validate(attrs)

        user = get_user_model().objects.get(username=attrs['username'])
        data.update({
            'access_token_expire': settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
            'refresh_life_time': settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
            'user_pk': user.pk
        })
        return data
