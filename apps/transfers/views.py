from rest_framework import mixins, permissions, viewsets

from . import models, serializers


class User2UserTransferViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    Endpoint for transferring of funds between users.
    """

    queryset = models.FundsMovement.objects.all()
    serializer_class = serializers.User2UserTransferSerializer

    permission_classes = (permissions.IsAuthenticated,)


class ReplenishmentFoundsViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    Endpoint for replenishment of funds to the account of the user.
    """

    queryset = models.FundsMovement.objects.all()
    serializer_class = serializers.ReplenishmentFundsSerializer

    permission_classes = (permissions.IsAuthenticated,)


class WithdrawingFoundsViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    Endpoint for withdrawing funds from the user account.
    """

    queryset = models.FundsMovement.objects.all()
    serializer_class = serializers.WithdrawingFoundsSerializer

    permission_classes = (permissions.IsAuthenticated,)

