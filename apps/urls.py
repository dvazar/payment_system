from django.urls import include, path


urlpatterns = [
    path('transfers/', include('apps.transfers.urls'),),
    path('users/', include('apps.users.urls'),),
]
