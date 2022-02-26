import fleep
import typing as tp

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from api.video.models import Video
from api.video.services_serializers import upload_video_to_aws


class VideoModelSerializer(serializers.ModelSerializer):
    """
    Model serializer for model video
    """

    file = serializers.FileField(required=True, write_only=True)

    def validate(self, attrs: tp.Dict[str, tp.Any]) -> tp.Dict[str, tp.Any]:
        """
        Validate all fields
        Args:
            attrs: attributes
        Returns:
            attributes
        """

        # get file and file info
        file = attrs.pop('file')
        file_bytes = file.read()
        file.seek(0)
        file_info = fleep.get(file_bytes)

        # validate file
        if not any(file_info.mime) or file_info.mime[0].split('/')[0] != 'video':
            raise ValidationError('File must be of the video type')

        # upload file to aws and get bucket path
        bucket_path = upload_video_to_aws(file_bytes=file_bytes, file_content_type=file_info.mime)
        attrs['bucket_path'] = bucket_path

        return attrs

    class Meta:
        model = Video
        fields = '__all__'
        read_only_fields = ['bucket_path']
