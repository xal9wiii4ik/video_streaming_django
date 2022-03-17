from django.db import models


class Video(models.Model):
    """
    Model for table video
    """

    title = models.CharField(max_length=100, verbose_name='title')
    description = models.TextField(max_length=1024, verbose_name='description')
    bucket_path = models.CharField(max_length=100, verbose_name='bucket path')
    upload_datetime = models.DateTimeField(auto_now_add=True, verbose_name='upload date time')
    delete_time = models.DateTimeField(null=True, blank=True, verbose_name='delete time')

    def __str__(self) -> str:
        return f'pk: {self.pk}, title: {self.title}'
