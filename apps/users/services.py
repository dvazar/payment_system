from typing import Optional

from django.db import transaction

from . import models


@transaction.atomic
def create_new_user(
    email: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> models.User:
    """
    Create a new user.
    """
    user = models.User.create_new_user(
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    return user
