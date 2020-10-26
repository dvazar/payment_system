from django.db import models, IntegrityError

from ..utils.exceptions import DomainException
from ..utils.models import TimeStampAbstract


class FundsMovement(TimeStampAbstract):
    """"""

    credit = models.ForeignKey(
        to='accounts.Account',
        on_delete=models.PROTECT,
        help_text='Source',
    )
    debit = models.ForeignKey(
        to='accounts.Account',
        on_delete=models.PROTECT,
        help_text='Destination',
    )
    amount = models.DecimalField(
        max_digits=19,
        decimal_places=2,
    )

    @classmethod
    def transfer_founds(cls, credit, debit, amount):
        """"""
        cls.objects.create(
            credit=credit,
            debit=debit,
            amount=amount,
        )
        try:
            credit.reduce_balance_on(amount)
        except IntegrityError as error:
            raise DomainException('Insufficient funds') from error
        debit.increase_balance_on(amount)
