from rest_framework import mixins, permissions, viewsets

from . import models, serializers


class UserViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    User endpoint.
    """

    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

    permission_classes = (permissions.IsAdminUser,)
