import uuid
from decimal import Decimal

from django.db import models, IntegrityError

from ..accounts.models import Account
from ..utils.exceptions import DomainException
from ..utils.models import TimeStampAbstract


class FundsMovement(TimeStampAbstract):
    """"""

    credit = models.ForeignKey(
        to='accounts.Account',
        on_delete=models.PROTECT,
        related_name='outgoing_transactions',
        related_query_name='outgoing_transaction',
        help_text='Source',
    )
    debit = models.ForeignKey(
        to='accounts.Account',
        on_delete=models.PROTECT,
        related_name='incoming_transactions',
        related_query_name='incoming_transaction',
        help_text='Destination',
    )
    amount = models.DecimalField(
        max_digits=19,
        decimal_places=2,
    )
    transaction_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text='ID of transaction',
    )

    @classmethod
    def transfer_founds(
        cls, *, credit: Account, debit: Account, amount: Decimal,
    ) -> 'FundsMovement':
        """
        Transfers funds from credit to debit.
        """
        transfer = cls.objects.create(
            credit=credit,
            debit=debit,
            amount=amount,
        )
        try:
            credit.reduce_balance_on(amount)
        except IntegrityError as error:
            raise DomainException('Insufficient funds') from error
        debit.increase_balance_on(amount)

        return transfer
