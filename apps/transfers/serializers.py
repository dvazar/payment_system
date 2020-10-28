from rest_framework import serializers

from ..users import models as user_models
from ..utils.fields import CustomPrimaryKey

from . import models, services


class User2UserTransferSerializer(serializers.ModelSerializer):
    """"""

    debit_user = CustomPrimaryKey(
        queryset=user_models.User.objects.select_related(
            'wallet',
        ),
        write_only=True,
    )

    class Meta:
        model = models.FundsMovement
        fields = (
            'debit_user', 'amount', 'transaction_id', 'created_at',
        )
        read_only_fields = (
            'transaction_id', 'created_at',
        )

    def create(self, validated_data):
        instance = services.user2user_transfer(
            credit=self.context['request'].user,
            debit=validated_data['debit_user'],
            amount=validated_data['amount'],
        )
        return instance


class ReplenishmentFundsSerializer(serializers.ModelSerializer):
    """"""

    class Meta:
        model = models.FundsMovement
        fields = (
            'amount', 'transaction_id', 'created_at',
        )
        read_only_fields = (
            'transaction_id', 'created_at',
        )

    def create(self, validated_data):
        instance = services.replenishment_founds(
            debit=self.context['request'].user,
            amount=validated_data['amount'],
        )
        return instance


class WithdrawingFoundsSerializer(serializers.ModelSerializer):
    """"""

    class Meta:
        model = models.FundsMovement
        fields = (
            'amount', 'transaction_id', 'created_at',
        )
        read_only_fields = (
            'transaction_id', 'created_at',
        )

    def create(self, validated_data):
        instance = services.withdrawing_founds(
            credit=self.context['request'].user,
            amount=validated_data['amount'],
        )
        return instance
