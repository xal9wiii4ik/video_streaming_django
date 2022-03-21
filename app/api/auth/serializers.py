import typing as tp

from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model, password_validation

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from api.auth.validation import validate_username_field, validate_email_field, validate_password_field
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
        return validate_username_field(username=username)

    @staticmethod
    def validate_email(email: str) -> str:
        return validate_email_field(email=email)

    @staticmethod
    def validate_password(password: str) -> str:
        return validate_password_field(password=password)

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
            'user_pk': user.pk,
            'access_token': data['access'],
            'refresh_token': data['refresh']
        })
        # TODO update data in flask application and remove del and rename access and refresh
        # TODO update refresh token in flask app
        del data['access']
        del data['refresh']
        return data


class AccountModelSerializer(serializers.ModelSerializer):
    """
    Model Serializer for model user
    """

    # @staticmethod
    # def validate_email(email):
    #     validate_email(value=email)
    #     is_exist = get_user_model().objects.filter(email=email).exists()
    #     if is_exist:
    #         raise serializers.ValidationError({'User with this email already exist'})
    #     return email
    #
    # @staticmethod
    # def validate_password(password: str) -> str:
    #     password_validation.validate_password(password=password)
    #     return password
    #
    # @staticmethod
    # def validate_username(username: str) -> str:
    #     is_exist = get_user_model().objects.filter(username=username).exists()
    #     if is_exist:
    #         raise serializers.ValidationError({'User with this username already exist'})
    #     return username

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

        attrs['password'] = make_password(password=attrs['password'])
        return attrs

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'is_staff']
        extra_kwargs = {
            'password': {'write_only': True},
            'is_staff': {'read_only': True}
        }


class UpdateAccountSerializer(serializers.Serializer):
    """
    Serializer for updating account credentials(include email, password, username)
    """

    username = serializers.CharField(max_length=100, required=False)
    password = serializers.CharField(max_length=500, required=False)
    email = serializers.CharField(max_length=100, required=False)
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)

    @staticmethod
    def validate_username(username: str) -> str:
        return validate_username_field(username=username)

    @staticmethod
    def validate_email(email: str) -> str:
        return validate_email_field(email=email)

    @staticmethod
    def validate_password(password: str) -> str:
        return validate_password_field(password=password)

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

        attrs['password'] = make_password(password=attrs['password'])
        return attrs
