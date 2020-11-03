from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.db import models

from ..accounts.models import Account


class User(AbstractUser):
    """"""

    wallet = models.OneToOneField(
        to='accounts.Account',
        on_delete=models.PROTECT,
        help_text='Wallet',
    )

    @classmethod
    def create_new_user(
        cls,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
    ) -> 'User':
        """
        Creates a new user.
        """
        user = cls.objects.create(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            wallet=Account.create_new_account(),
        )
        return user

    def get_locked_wallet(self, nowait=False) -> Account:
        """
        Returns the locked user's wallet.
        """
        wallet = Account.objects.select_for_update(
            nowait=nowait,
        ).get(
            user=self,
        )
        return wallet
