import decimal
import typing

from django.db import transaction

from ..accounts.models import Account
from ..utils.exceptions import DomainException

from .models import FundsMovement

if typing.TYPE_CHECKING:
    from ..users.models import User


@transaction.atomic
def user2user_transfer(
    credit: User,
    debit: User,
    amount: decimal.Decimal,
):
    """
    Transferring funds between users.
    """
    if credit.wallet.balance < amount:
        raise DomainException('Insufficient funds')

    transfer = FundsMovement.transfer_founds(credit, debit, amount)

    return transfer


@transaction.atomic
def transfer_founds(debit, amount):
    """
    Transfer of funds to the account of the user (from an ATM, for instance).
    """
    credit = Account.get_bank_account()
    transfer = FundsMovement.transfer_founds(credit, debit, amount)

    return transfer


@transaction.atomic
def withdrawing_founds(credit, amount):
    """
    Withdrawing funds from the user account.
    """
    if credit.wallet.balance < amount:
        raise DomainException('Insufficient funds')

    debit = Account.get_bank_account()
    transfer = FundsMovement.transfer_founds(credit, debit, amount)

    return transfer
