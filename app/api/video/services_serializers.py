import boto3
import typing as tp

from datetime import datetime

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

    datetime_now = datetime.now().strftime('%Y-%m-%d:%H-%M-%S.%f')
    # TODO add username
    file_path = f'username/{datetime_now}.{file_content_type[0].split("/")[-1]}'

    file = bucket.put_object(Key=file_path,
                             Body=file_bytes,
                             ContentType=file_content_type[0])

    bucket_path = f'https://s3-{settings.BUCKET_REGION}.amazonaws.com/{settings.VIDEOS_BUCKET}/{file.key}'
    return bucket_path
