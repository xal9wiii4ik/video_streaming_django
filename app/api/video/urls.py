from rest_framework.routers import SimpleRouter


from api.video.views import VideoModelViewSet


router = SimpleRouter()

router.register('video', VideoModelViewSet)

urlpatterns = router.urls
