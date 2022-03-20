from django.urls import path

from api.auth.views import RegisterUserApiView

urlpatterns = [
    path('account/register/', RegisterUserApiView.as_view(), name='register'),
]
