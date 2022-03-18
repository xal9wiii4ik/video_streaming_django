import json

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api.video.models import Video


class SetupAPITestCase(APITestCase):
    """ SetUp tests """

    def setUp(self) -> None:
        # creating users and tokens for users

        password = make_password('password')
        url = reverse('token')

        self.user_1 = get_user_model().objects.create(username='user_1',
                                                      is_staff=True,
                                                      password=password,
                                                      is_active=True,
                                                      email='user_1@mail.ru')
        data = {
            'username': self.user_1.username,
            'password': 'password'
        }
        json_data = json.dumps(data)
        token_data = self.client.post(path=url, data=json_data, content_type='application/json').data
        self.token_1 = f'Token ' \
                       f'{token_data["access"]}'

        self.user_2 = get_user_model().objects.create(username='user_2',
                                                      password=password,
                                                      is_active=True,
                                                      email='user_2@mail.ru')
        data = {
            'username': self.user_2.username,
            'password': 'password'
        }
        json_data = json.dumps(data)
        token_data = self.client.post(path=url, data=json_data, content_type='application/json').data
        self.token_2 = f'Token ' \
                       f'{token_data["access"]}'

        self.user_3 = get_user_model().objects.create(username='user_3',
                                                      password=password,
                                                      is_active=True,
                                                      email='user_3@mail.ru')
        data = {
            'username': self.user_3.username,
            'password': 'password'
        }
        json_data = json.dumps(data)
        token_data = self.client.post(path=url, data=json_data, content_type='application/json').data
        self.token_3 = f'Token ' \
                       f'{token_data["access"]}'

        # creating videos
        self.video_1 = Video.objects.create(
            title='title_1',
            description='description_1',
            bucket_path='bucket_path_1'
        )
        self.video_2 = Video.objects.create(
            title='title_2',
            description='description_2',
            bucket_path='bucket_path_2'
        )
