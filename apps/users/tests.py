from rest_framework import status, test

from django.urls import reverse

from . import models


class TestUserEndpoint(test.APITestCase):
    """
    Testing a user endpoint.
    """

    expected_fields = {
        'id', 'email', 'first_name', 'last_name', 'wallet',
    }
    wallet_expected_fields = {
        'number', 'balance',
    }

    def setUp(self):
        super().setUp()
        self.list_url = reverse('user-list')

    def test_create__successful_outcome(self):

        data = {
            'email': 'uncle-bob@gmail.com',
            'first_name': 'Robert',
            'last_name': 'Cecil',
        }

        resp = self.client.post(self.list_url, data)
        self.assertEqual(
            resp.status_code, status.HTTP_201_CREATED, resp.content,
        )
        self.assertSetEqual(set(resp.data), self.expected_fields)
        self.assertSetEqual(
            set(resp.data['wallet']), self.wallet_expected_fields,
        )
        for fld in ('email', 'first_name', 'last_name'):
            self.assertEqual(resp.data[fld], data[fld])

        # Checks user in DB:
        user = models.User.objects.filter(pk=resp.data['id']).first()
        self.assertIsNotNone(user)
        for fld in ('email', 'first_name', 'last_name'):
            self.assertEqual(resp.data[fld], getattr(user, fld))

    def test_create__failed_cuz_user_already_created_and_authenticated(self):

        user = models.User.create_new_user(
            email='f.martin@yandex.com',
            first_name='Martin',
            last_name='Fowler',
        )

        data = {
            'email': 'foo-bar@gmail.com',
            'first_name': 'Foo',
            'last_name': 'Bar',
        }

        self.client.force_login(user)

        resp = self.client.post(self.list_url, data)
        self.assertEqual(
            resp.status_code, status.HTTP_403_FORBIDDEN, resp.content,
        )
