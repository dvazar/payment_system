import decimal
import uuid

from django.conf import settings
from django.core import validators
from django.db import models

from ..utils.models import TimeStampAbstract


class Account(TimeStampAbstract):
    """"""

    account_number = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )
    balance = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        default=0,
        validators=(
            validators.MinValueValidator(0),
        ),
    )

    class Meta:
        constraints = [
            # Make sure the balance is at least zero
            models.CheckConstraint(
                check=models.Q(
                    balance__gte=decimal.Decimal('0'),
                ),
                name='balance_gte_0',
            ),
        ]

    @classmethod
    def get_bank_account(cls) -> 'Account':
        account = cls.objects.get_or_create(
            account_number=uuid.UUID(settings.BANK_ACCOUNT_ID),
            defaults={
                'balance': decimal.Decimal(str(settings.BANK_BALANCE)),
            },
        )
        return account

    @classmethod
    def create_new_account(cls) -> 'Account':
        account = cls.objects.create()
        return account

    def increase_balance_on(self, amount: decimal.Decimal):
        self.balance += amount
        self.save(update_fields=('balance',))

    def reduce_balance_on(self, amount: decimal.Decimal):
        self.balance -= amount
        self.save(update_fields=('balance',))
