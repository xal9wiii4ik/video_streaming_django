import json

from django.contrib.auth.hashers import check_password
from rest_framework.reverse import reverse

from api.utils.setup_tests import SetupAPITestCase


class AccountViewTest(SetupAPITestCase):
    """
    Test Cases for view account
    """

    def test_get(self) -> None:
        """
        Get accounts lists
        """

        url = reverse('auth:user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        expected_data = [
            {
                'id': self.user_1.pk,
                'username': 'user_1',
                'email': 'user_1@mail.ru',
                'first_name': '',
                'last_name': '',
                'is_staff': True
            },
            {
                'id': self.user_2.pk,
                'username': 'user_2',
                'email': 'user_2@mail.ru',
                'first_name': '',
                'last_name': '',
                'is_staff': False
            },
            {
                'id': self.user_3.pk,
                'username': 'user_3',
                'email': 'user_3@mail.ru',
                'first_name': '',
                'last_name': '',
                'is_staff': False
            }
        ]
        self.assertEqual(response.json(), expected_data)

    def test_retrieve(self) -> None:
        """
        Test get account retrieve
        """

        url = reverse('auth:user-detail', args=(self.user_1.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        expected_data = {
            'id': self.user_1.pk,
            'username': 'user_1',
            'email': 'user_1@mail.ru',
            'first_name': '',
            'last_name': '',
            'is_staff': True
        }
        self.assertEqual(response.json(), expected_data)

    def test_update_not_authenticated(self) -> None:
        """
        Update not authenticated
        """

        url = reverse('auth:user-detail', args=(self.user_1.pk,))
        data = {
            'email': 'new_email@123'
        }
        json_data = json.dumps(data)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_update_not_owner(self) -> None:
        """
        Update not owner
        """

        url = reverse('auth:user-detail', args=(self.user_1.pk,))
        data = {
            'email': 'new_email@123.ru',
            'password': 'somepasswordasd123123'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token_2)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_update_owner(self) -> None:
        """
        Update owner
        """

        url = reverse('auth:user-detail', args=(self.user_1.pk,))
        data = {
            'password': 'new_password_123-a',
            'first_name': 'Nikita',
            'email': 'new_email@123.ru'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.patch(url, data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.user_1.refresh_from_db()
        self.assertEqual(self.user_1.first_name, 'Nikita')
        self.assertEqual(self.user_1.email, 'new_email@123.ru')
        self.assertTrue(check_password('new_password_123-a', self.user_1.password))
