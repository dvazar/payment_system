from rest_framework.routers import SimpleRouter

from django.urls import path

from . import views


router = SimpleRouter()


urlpatterns = [
    path(
        'user2user/', views.User2UserTransferViewSet.as_view(
            {'post': 'create'},
        ),
        name='user2user-transfer',
    ),
    path(
        'replenishment-founds/', views.ReplenishmentFoundsViewSet.as_view(
            {'post': 'create'},
        ),
        name='replenishment-founds',
    ),
    path(
        'withdrawing-founds/', views.WithdrawingFoundsViewSet.as_view(
            {'post': 'create'},
        ),
        name='withdrawing-founds',
    ),
]
