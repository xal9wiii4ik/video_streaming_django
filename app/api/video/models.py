from django.db import models


class Video(models.Model):
    """
    Model for table video
    """

    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1024)
    bucket_path = models.CharField(max_length=100)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'pk: {self.pk}'
