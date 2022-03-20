import typing as tp

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from api.auth.serializers import RegisterUserSerializer, CustomTokenObtainPairSerializer
from api.auth.services import create_new_user


class RegisterUserApiView(APIView):
    """
    Api View for creating new user
    """

    @swagger_auto_schema(request_body=RegisterUserSerializer)
    def post(self, request: Request, *args: tp.Any, **kwargs: tp.Any) -> Response:
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = serializer.data
        create_new_user(data=serializer_data)
        return Response(data=serializer_data, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for token
    """

    serializer_class = CustomTokenObtainPairSerializer
