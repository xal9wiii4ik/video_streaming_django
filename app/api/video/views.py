import typing as tp

from django.utils import timezone

from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.video.models import Video
from api.video.serializers import VideoModelSerializer
from api.video.services_serializers import validate_file
from api.video.services_views import upload_video_to_aws


class VideoModelViewSet(ModelViewSet):
    """
    Model View set for model video
    """

    queryset = Video.objects.filter(delete_time__isnull=True)
    serializer_class = VideoModelSerializer
    parser_classes = (MultiPartParser,)
    # TODO add permissions

    def perform_create(self, serializer: VideoModelSerializer) -> None:
        # validate file
        file_bytes, file_mime = validate_file(data=serializer.validated_data)
        # upload file to aws bucket
        bucket_path = upload_video_to_aws(
            file_bytes=file_bytes,
            file_content_type=file_mime
        )
        # set bucket path
        serializer.validated_data['bucket_path'] = bucket_path
        # TODO add user
        serializer.save()

    def destroy(self, request: Request, *args: tp.Any, **kwargs: tp.Any) -> Response:
        video = Video.objects.filter(pk=kwargs.get('pk'))
        if not video:
            return Response(data={"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        video = video[0]
        video.delete_time = timezone.now()
        video.save()
        return Response(data={'delete_time': video.delete_time}, status=status.HTTP_204_NO_CONTENT)
