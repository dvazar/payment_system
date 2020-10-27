from decimal import Decimal

from django.db import transaction

from ..accounts.models import Account
from ..users.models import User
from ..utils.exceptions import DomainException

from . import models


@transaction.atomic
def user2user_transfer(
    *,
    credit: User,
    debit: User,
    amount: Decimal,
) -> models.FundsMovement:
    """
    Internal transferring funds between users.
    """
    if credit.wallet.balance < amount:
        raise DomainException('Insufficient funds')

    transfer = models.FundsMovement.transfer_founds(
        credit=credit.wallet,
        debit=debit.wallet,
        amount=amount,
    )

    return transfer


@transaction.atomic
def replenishment_founds(debit: User, amount: Decimal) -> models.FundsMovement:
    """
    Replenishment of funds to the account of the user (from an ATM,
    for instance).
    """
    credit = Account.get_bank_account()
    transfer = models.FundsMovement.transfer_founds(
        credit=credit,
        debit=debit.wallet,
        amount=amount,
    )

    return transfer


@transaction.atomic
def withdrawing_founds(credit: User, amount: Decimal) -> models.FundsMovement:
    """
    Withdrawing funds from the user account.
    """
    if credit.wallet.balance < amount:
        raise DomainException('Insufficient funds')

    debit = Account.get_bank_account()
    transfer = models.FundsMovement.transfer_founds(
        credit=credit.wallet,
        debit=debit,
        amount=amount,
    )

    return transfer
