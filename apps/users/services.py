from django.contrib.auth import get_user_model
from django.db import transaction


UserModel = get_user_model()


@transaction.atomic
def create_new_user(email: str, first_name: str, last_name: str):
    """
    Create a new user.
    """

    user = UserModel.create_new_user(
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    return user
