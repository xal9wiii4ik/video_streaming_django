import boto3
import typing as tp

from django.utils import timezone

from base import settings


def upload_video_to_aws(file_bytes: bytes, file_content_type: tp.List[str]) -> str:
    """
    Upload video to aws
    Args:
        file_bytes: file bytes
        file_content_type: file content type
    Return:
        current bucket path
    """

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(settings.VIDEOS_BUCKET)

    # TODO add username
    file_extension = file_content_type[0].split("/")[-1]
    file_path = f'username/{timezone.now():{settings.BASE_DATETIME_FORMAT}}.{file_extension}'

    file = bucket.put_object(Key=file_path,
                             Body=file_bytes,
                             ContentType=file_content_type[0])

    bucket_path = settings.BUCKET_PATH.format(file.key)
    return bucket_path
