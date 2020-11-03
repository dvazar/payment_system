from decimal import Decimal

from django.db import transaction, OperationalError

from ..accounts.models import Account
from ..users.models import User
from ..utils.exceptions import DomainException
from ..utils.functools import retry

from . import models


@retry(exceptions=(OperationalError,))
@transaction.atomic
def user2user_transfer(
    *,
    credit: User,
    debit: User,
    amount: Decimal,
) -> models.FundsMovement:
    """
    Internal transferring funds between users.

    Note: To avoid deadlocks in this operation, we cannot determine the order
    of acquiring a lock, so we will apply the technique of not waiting for a
    lock, and we will repeat the call of this function N times.
    """
    credit_wallet = credit.get_locked_wallet(nowait=True)
    if credit_wallet.balance < amount:
        raise DomainException('Insufficient funds')

    debit_wallet = debit.get_locked_wallet(nowait=True)

    transfer = models.FundsMovement.transfer_founds(
        credit=credit_wallet,
        debit=debit_wallet,
        amount=amount,
    )

    return transfer


@transaction.atomic
def replenishment_founds(debit: User, amount: Decimal) -> models.FundsMovement:
    """
    Replenishment of funds to the account of the user (from an ATM,
    for instance).

    Note: To avoid deadlocks in withdrawal and replenishment operations, we
    will request locks (waitable lock) uniformly, first we block the user's
    wallet, and then the bank account.
    """
    debit_wallet = debit.get_locked_wallet(nowait=False)
    credit_wallet = Account.get_bank_account(nowait=False)

    transfer = models.FundsMovement.transfer_founds(
        credit=credit_wallet,
        debit=debit_wallet,
        amount=amount,
    )

    return transfer


@transaction.atomic
def withdrawing_founds(credit: User, amount: Decimal) -> models.FundsMovement:
    """
    Withdrawing funds from the user account.

    Note: To avoid deadlocks in withdrawal and replenishment operations, we
    will request locks (waitable lock) uniformly, first we block the user's
    wallet, and then the bank account.
    """
    credit_wallet = credit.get_locked_wallet(nowait=False)

    if credit_wallet.balance < amount:
        raise DomainException('Insufficient funds')

    debit_wallet = Account.get_bank_account(nowait=False)

    transfer = models.FundsMovement.transfer_founds(
        credit=credit_wallet,
        debit=debit_wallet,
        amount=amount,
    )

    return transfer
