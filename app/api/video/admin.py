import typing as tp

from django.contrib import admin
from django.utils.safestring import mark_safe, SafeString

from api.video.models import Video


@admin.register(Video)
class VideoModelAdmin(admin.ModelAdmin):
    """
    Display video on admin panel
    """

    list_display = ('pk', 'title', 'upload_date', 'delete_time')
