"""payment_system URL Configuration
"""
from django.urls import include, path

urlpatterns = [
    path('^transfers/', include('apps.transfers')),
    path('^users/', include('apps.users')),
]
