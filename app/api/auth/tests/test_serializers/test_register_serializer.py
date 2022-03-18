from rest_framework.exceptions import ValidationError, ErrorDetail

from api.auth.serializers import RegisterUserSerializer
from api.utils.setup_tests import SetupAPITestCase


class RegisterUserTestCase(SetupAPITestCase):
    """
    Test Case for serializer register user
    """

    def test_exist_username(self) -> None:
        try:
            data = {
                'password': 'aksjdakmdl2',
                'repeat_password': 'aksjdakmdl2',
                'email': 'some@email.ru',
                'first_name': 'first_name',
                'last_name': 'last_name',
                'username': 'user_1'
            }
            serializer = RegisterUserSerializer(data=data)
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            expected_exception = {
                'username': [ErrorDetail(string="{'User with this username already exist'}", code='invalid')]
            }
            self.assertEqual(expected_exception, e.detail)

    def test_exist_email(self) -> None:
        try:
            data = {
                'password': 'aksjdakmdl2',
                'repeat_password': 'aksjdakmdl2',
                'email': 'user_1@mail.ru',
                'first_name': 'first_name',
                'last_name': 'last_name',
                'username': 'test_register_serializer_username'
            }
            serializer = RegisterUserSerializer(data=data)
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            expected_exception = {
                'email': [ErrorDetail(string="{'User with this email already exist'}", code='invalid')]
            }
            self.assertEqual(expected_exception, e.detail)

    def test_not_equal_repeat_password(self) -> None:
        try:
            data = {
                'password': 'aksjdakmdl2',
                'repeat_password': 'aksjdakml2',
                'email': 'user_11@mail.ru',
                'first_name': 'first_name',
                'last_name': 'last_name',
                'username': 'test_register_serializer_username'
            }
            serializer = RegisterUserSerializer(data=data)
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            expected_exception = {
                'repeat_password': [ErrorDetail(string='Repeat password should be equal to password', code='invalid')]
            }
            self.assertEqual(expected_exception, e.detail)
