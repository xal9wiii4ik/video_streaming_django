import typing as tp

from django.contrib.auth import get_user_model


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
