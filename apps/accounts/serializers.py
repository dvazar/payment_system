from rest_framework import serializers

from . import models


class AccountSimpleSerializer(serializers.ModelSerializer):
    """"""

    number = serializers.ReadOnlyField(
        source='account_number',
    )

    class Meta:
        model = models.Account
        fields = (
            'number', 'balance',
        )
