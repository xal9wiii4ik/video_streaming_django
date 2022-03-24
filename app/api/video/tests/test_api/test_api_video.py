import mock

from django.core.files import File

from rest_framework import status
from rest_framework.reverse import reverse

from api.utils.utils_tests.setup_tests import SetupAPITestCase


class VideoAPITestCase(SetupAPITestCase):
    """
    Test Cases for Video CRUD
    """

    def test_get_list(self) -> None:
        """
        Get list with videos
        """

        url = reverse('video:video-list')
        response = self.client.get(path=url)
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)
        response_data = response.json()
        for data in response_data:
            del data['upload_datetime']
        expected_data = [
            {
                'id': self.video_1.pk,
                'title': 'title_1',
                'description': 'description_1',
                'bucket_path': 'bucket_path_1',
                'delete_time': None,
                'account': self.user_1.pk,
                'username': 'user_1'
            },
            {
                'id': self.video_2.pk,
                'title': 'title_2',
                'description': 'description_2',
                'bucket_path': 'bucket_path_2',
                'delete_time': None,
                'account': self.user_2.pk,
                'username': 'user_2'
            }
        ]
        self.assertEqual(first=expected_data, second=response_data)

    def test_get_retrieve(self) -> None:
        """
        Get retrieve video
        """

        url = reverse('video:video-detail', args=(self.video_1.pk,))
        response = self.client.get(path=url)
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)
        response_data = response.json()
        del response_data['upload_datetime']
        expected_data = {
            'id': self.video_1.pk,
            'title': 'title_1',
            'description': 'description_1',
            'bucket_path': 'bucket_path_1',
            'delete_time': None,
            'account': self.user_1.pk,
            'username': 'user_1'
        }
        self.assertEqual(first=expected_data, second=response_data)

    def test_update_not_authenticated(self) -> None:
        """
        Update video not authenticated
        """

        url = reverse('video:video-detail', args=(self.video_1.pk,))
        self.assertEqual(first='title_1', second=self.video_1.title)
        data = {
            'title': 'new_title'
        }
        response = self.client.patch(path=url, data=data)
        self.assertEqual(first=status.HTTP_401_UNAUTHORIZED, second=response.status_code)

    def test_update_not_owner(self) -> None:
        """
        Update video not owner
        """

        url = reverse('video:video-detail', args=(self.video_1.pk,))
        self.assertEqual(first='title_1', second=self.video_1.title)
        data = {
            'title': 'new_title'
        }
        self.client.credentials(HTTP_AUTHORIZATION=self.token_2)
        response = self.client.patch(path=url, data=data)
        self.assertEqual(first=status.HTTP_403_FORBIDDEN, second=response.status_code)

    def test_update_owner(self) -> None:
        """
        Update video
        """

        url = reverse('video:video-detail', args=(self.video_1.pk,))
        self.assertEqual(first='title_1', second=self.video_1.title)
        data = {
            'title': 'new_title'
        }
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.patch(path=url, data=data)
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)
        self.video_1.refresh_from_db()
        self.assertEqual(first='new_title', second=self.video_1.title)

    def test_create(self) -> None:
        """
        Test Create
        """

        url = reverse('video:video-list')
        with open('api/utils/utils_tests/videoplayback.mp4', 'rb') as f:
            data = {
                'title': 'tile',
                'description': 'description',
                'file': f
            }
            self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
            response = self.client.post(url, data=data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_not_valid_file(self) -> None:
        """
        Test Create not valid file
        """

        image_mock = mock.MagicMock(spec=File)
        image_mock.name = 'image.png'

        url = reverse('video:video-list')
        data = {
            'title': 'tile',
            'description': 'description',
            'file': image_mock
        }
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.post(url, data=data)
        self.assertEqual(response.json(), ['File must be of the video type'])

    def test_delete(self) -> None:
        """
        Delete video
        """

        url = reverse('video:video-detail', args=(self.video_1.pk,))
        self.assertIsNone(self.video_1.delete_time)
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.delete(path=url)
        self.assertEqual(first=status.HTTP_204_NO_CONTENT, second=response.status_code)
        self.video_1.refresh_from_db()
        self.assertIsNotNone(self.video_1.delete_time)

    def test_delete_not_found(self) -> None:
        """
        Delete video
        """

        url = reverse('video:video-detail', args=(-1,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.delete(path=url)
        self.assertEqual(first=status.HTTP_404_NOT_FOUND, second=response.status_code)
