from rest_framework.routers import SimpleRouter

from . import views


router = SimpleRouter()

task_occur_router = router.register(
    prefix='',
    viewset=views.UserViewSet,
    basename='user',
)

urlpatterns = [
    *router.urls,
]
