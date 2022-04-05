from rest_framework_simplejwt.views import TokenRefreshView

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from base.yasg import urlpatterns as doc_urls
from api.auth.views import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(('api.video.urls', 'video'), namespace='video')),
    path('api/', include(('api.auth.urls', 'auth'), namespace='auth')),
    path('auth/token/', CustomTokenObtainPairView.as_view(), name='token'),
    path('auth/token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += doc_urls
