from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from base import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(('api.video.urls', 'video'), namespace='video')),
]

urlpatterns += staticfiles_urlpatterns()
