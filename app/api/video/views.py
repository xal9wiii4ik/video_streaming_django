import typing as tp

from rest_framework.parsers import MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.video.models import Video
from api.video.serializers import VideoModelSerializer


class VideoModelViewSet(ModelViewSet):
    """
    Model View set for model video
    """

    # TODO add filer for soft delete
    queryset = Video.objects.all()
    serializer_class = VideoModelSerializer
    parser_classes = (MultiPartParser,)
    # TODO add permissions

    def create(self, request: Request, *args: tp.Any, **kwargs: tp.Any) -> Response:
        return super(VideoModelViewSet, self).create(request, *args, **kwargs)
