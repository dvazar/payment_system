from rest_framework import serializers

from ..accounts.serializers import AccountSimpleSerializer

from . import models, services


class UserSerializer(serializers.ModelSerializer):
    """"""

    email = serializers.EmailField(
        required=True,
        allow_null=False,
        allow_blank=False,
    )
    wallet = AccountSimpleSerializer(
        read_only=True,
        help_text='Wallet',
    )

    class Meta:
        model = models.User
        fields = (
            'id', 'email', 'first_name', 'last_name', 'wallet',
        )

    def create(self, validated_data):
        instance = services.create_new_user(**validated_data)
        return instance
