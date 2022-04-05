import typing as tp

from rest_framework.serializers import SerializerMetaclass

from django.contrib.auth import get_user_model


def process_request_data(serializer_class: SerializerMetaclass, data: tp.Dict[str, tp.Any]) -> tp.Dict[str, tp.Any]:
    """
    Process request data
    Args:
        serializer_class: current serializer
        data: request data
    Raise:
        serializer validation exception
    Returns:
        dict with validate fields
    """

    serializer = serializer_class(data=data)
    serializer.is_valid(raise_exception=True)
    serializer_data: tp.Dict[str, tp.Any] = serializer.data
    return serializer_data


def create_new_user(data: tp.Dict[str, tp.Any]) -> None:
    """
    Create new user and update returned user data
    Args:
        data: new user data
    """

    del data['repeat_password']
    user = get_user_model().objects.create(**data)
    del data['password']
    data['id'] = user.id


def update_account_data(data: tp.Dict[str, tp.Any], pk: int) -> None:
    """
    Update account data
    """

    if data:
        get_user_model().objects.filter(pk=pk).update(**data)
