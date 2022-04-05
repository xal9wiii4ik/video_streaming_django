from rest_framework import serializers

from django.core.validators import validate_email
from django.contrib.auth import get_user_model, password_validation


def validate_username_field(username: str) -> str:
    """
    Validate username field
    Args:
        username: username
    Raise:
        ValidationError if user with this username already exist
    Returns:
        username if field is valid
    """

    is_exist = get_user_model().objects.filter(username=username).exists()
    if is_exist:
        raise serializers.ValidationError({'User with this username already exist'})
    return username


def validate_email_field(email: str) -> str:
    """
    Validate email field
    Args:
        email: email
    Raise:
        ValidationError if field is not valid or user with this email already exist
    Returns:
        email if field is valid
    """

    validate_email(value=email)
    is_exist = get_user_model().objects.filter(email=email).exists()
    if is_exist:
        raise serializers.ValidationError({'User with this email already exist'})
    return email


def validate_password_field(password: str) -> str:
    """
    Validate password field
    Args:
        password: email
    Raise:
        ValidationError if field is not valid
    Returns:
        password if field is valid
    """

    # django will raise exception if bad value
    password_validation.validate_password(password=password)
    return password
