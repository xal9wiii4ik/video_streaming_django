import typing as tp

from drf_yasg.utils import swagger_auto_schema

from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework import mixins
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from api.auth.permissions import IsOwnerOrReadOnlyAccountPermission
from api.auth.serializers import (
    RegisterUserSerializer,
    CustomTokenObtainPairSerializer,
    AccountModelSerializer,
    UpdateAccountSerializer,
)
from api.auth.services import create_new_user, update_account_data, process_request_data


class RegisterUserApiView(APIView):
    """
    Api View for creating new user
    """

    @swagger_auto_schema(request_body=RegisterUserSerializer)
    def post(self, request: Request, *args: tp.Any, **kwargs: tp.Any) -> Response:
        serializer_data = process_request_data(serializer_class=RegisterUserSerializer, data=request.data)
        create_new_user(data=serializer_data)
        return Response(data=serializer_data, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for token
    """

    serializer_class = CustomTokenObtainPairSerializer


class AccountModelViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.UpdateModelMixin,
                          GenericViewSet):
    """
    Model View set for account
    """

    queryset = get_user_model().objects.all()
    serializer_class = AccountModelSerializer
    permission_classes = (IsOwnerOrReadOnlyAccountPermission,)

    def update(self, request: Request, *args: tp.Any, **kwargs: tp.Any) -> Response:
        # check permissions using object(has_object_permission)
        self.get_object()

        request_data = request.data.copy()

        # serializer does not provide verification of the presence of values already in the user fields
        # if true they will be deleted
        if request_data.get('username') is not None and request_data.get('username') == request.user.username:
            del request_data['username']
        if request_data.get('email') is not None and request_data.get('email') == request.user.email:
            del request_data['email']

        serializer_data = process_request_data(serializer_class=UpdateAccountSerializer, data=request_data)
        update_account_data(data=serializer_data, pk=kwargs['pk'])
        return Response(data=request.data, status=status.HTTP_200_OK)
