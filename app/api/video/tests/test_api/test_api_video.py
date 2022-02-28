import json

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from api.video.models import Video


class VideoAPITestCase(APITestCase):
    """
    Test Case for Video CRUD
    """

    def setUp(self) -> None:
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

    def test_get_list(self) -> None:
        """
        Get list with videos
        """

        url = reverse('video:video-list')
        response = self.client.get(path=url)
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)
        response_data = response.json()
        for data in response_data:
            del data['upload_date']
        expected_data = [
            {
                'id': self.video_1.pk,
                'title': 'title_1',
                'description': 'description_1',
                'bucket_path': 'bucket_path_1',
                'delete_time': None
            },
            {
                'id': self.video_2.pk,
                'title': 'title_2',
                'description': 'description_2',
                'bucket_path': 'bucket_path_2',
                'delete_time': None
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
        del response_data['upload_date']
        expected_data = {
            'id': self.video_1.pk,
            'title': 'title_1',
            'description': 'description_1',
            'bucket_path': 'bucket_path_1',
            'delete_time': None
        }
        self.assertEqual(first=expected_data, second=response_data)

    def test_update(self) -> None:
        """
        Update video
        """

        url = reverse('video:video-detail', args=(self.video_1.pk,))
        self.assertEqual(first='title_1', second=self.video_1.title)
        data = {
            'title': 'new_title'
        }
        response = self.client.patch(path=url, data=data)
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)
        self.video_1.refresh_from_db()
        self.assertEqual(first='new_title', second=self.video_1.title)

    def test_delete(self) -> None:
        """
        Delete video
        """

        url = reverse('video:video-detail', args=(self.video_1.pk,))
        self.assertIsNone(self.video_1.delete_time)
        response = self.client.delete(path=url)
        self.assertEqual(first=status.HTTP_204_NO_CONTENT, second=response.status_code)
        self.video_1.refresh_from_db()
        self.assertIsNotNone(self.video_1.delete_time)

    def test_delete_not_found(self) -> None:
        """
        Delete video
        """

        url = reverse('video:video-detail', args=(-1,))
        response = self.client.delete(path=url)
        self.assertEqual(first=status.HTTP_404_NOT_FOUND, second=response.status_code)
