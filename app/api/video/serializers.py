from rest_framework import serializers

from api.video.models import Video


class VideoModelSerializer(serializers.ModelSerializer):
    """
    Model serializer for model video
    """

    file = serializers.FileField(required=False, write_only=True)

    class Meta:
        model = Video
        fields = '__all__'
        read_only_fields = ['bucket_path', 'upload_datetime', 'delete_time', 'account']
