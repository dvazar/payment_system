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
        self.admin = models.User.objects.create_superuser(
            username='admin',
            email='admin@payment-system.com',
            password='secrete-pass',
        )

    def test_create(self):

        self.client.force_login(self.admin)

        data = {
            'email': 'uncle-bob@payment-system.com',
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
