from django.urls import path

from api.auth.views import RegisterUserApiView, AccountModelViewSet

from rest_framework.routers import SimpleRouter


router = SimpleRouter()

router.register('account', AccountModelViewSet)

urlpatterns = [
    path('account/register/', RegisterUserApiView.as_view(), name='register'),
]

urlpatterns += router.urls
