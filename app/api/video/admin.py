import typing as tp

from django.contrib import admin
from django.utils.safestring import mark_safe, SafeString

from api.video.models import Video


@admin.register(Video)
class VideoModelAdmin(admin.ModelAdmin):
    """
    Display video on admin panel
    """

    @staticmethod
    def display_file(obj: Video) -> tp.Union[SafeString, str]:
        """
        Display file on admin panel
        Args:
            obj: current obj of Video
        Returns:
            SafeString: class which video on admin panel
        """

        return mark_safe(f'<video controls="controls"'
                         f'<source :src="{obj.bucket_path}" type="video/mp4">'
                         f'</video>')

    list_display = ('pk', 'title', 'upload_date')
