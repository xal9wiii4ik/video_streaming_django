from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from api.auth.views import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(('api.video.urls', 'video'), namespace='video')),
    path('api/', include(('api.auth.urls', 'auth'), namespace='auth')),
    path('token/', CustomTokenObtainPairView.as_view(), name='token'),
]

urlpatterns += staticfiles_urlpatterns()
