from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.db import models

from ..accounts.models import Account


class User(AbstractUser):
    """"""

    wallet = models.OneToOneField(
        to='accounts.Account',
        on_delete=models.PROTECT,
        null=True,
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
