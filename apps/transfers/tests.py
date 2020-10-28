from decimal import Decimal

from rest_framework import status, test

from django.urls import reverse

from ..users import models as user_models


class TestUser2UserTransferEndpoint(test.APITestCase):
    """
    Testing an endpoint for transferring of funds between users.
    """

    expected_fields = {
        'amount', 'transaction_id', 'created_at',
    }
    error_expected_fields = {
        'code', 'message',
    }

    def setUp(self):
        super().setUp()
        self.url = reverse('user2user-transfer')

        self.UncleBob = user_models.User.create_new_user(
            email='uncle-bob@gmail.com',
            first_name='Robert',
            last_name='Cecil',
        )
        self.MartinFowler = user_models.User.create_new_user(
            email='f.martin@yandex.com',
            first_name='Martin',
            last_name='Fowler',
        )

    def test_u2u_transfer__successful_outcome(self):

        self.UncleBob.wallet.increase_balance_on(Decimal('1000'))

        data = {
            'debit_user': self.MartinFowler.pk,
            'amount': '500.50',
        }

        self.client.force_login(self.UncleBob)

        resp = self.client.post(self.url, data)
        self.assertEqual(
            resp.status_code, status.HTTP_201_CREATED, resp.content,
        )
        self.assertSetEqual(set(resp.data), self.expected_fields)

        # Checks in DB:
        self.UncleBob.wallet.refresh_from_db()
        self.assertEqual(self.UncleBob.wallet.balance, Decimal('499.50'))

        self.MartinFowler.wallet.refresh_from_db()
        self.assertEqual(self.MartinFowler.wallet.balance, Decimal('500.50'))

    def test_u2u_transfer__failed_cuz_not_enough_funds(self):
        self.UncleBob.wallet.increase_balance_on(Decimal('1000'))

        data = {
            'debit_user': self.MartinFowler.pk,
            'amount': '1000.01',
        }

        self.client.force_login(self.UncleBob)

        resp = self.client.post(self.url, data)
        self.assertEqual(
            resp.status_code, status.HTTP_400_BAD_REQUEST, resp.content,
        )
        data = resp.json()
        self.assertSetEqual(set(data), self.error_expected_fields)
        self.assertEqual(data['code'], 'invalid')
        self.assertEqual(data['message'], 'Insufficient funds')


class TestReplenishmentFundsEndpoint(test.APITestCase):
    """
    Testing an endpoint for replenishment of funds to the account of the user.
    """

    expected_fields = {
        'amount', 'transaction_id', 'created_at',
    }
    error_expected_fields = {
        'code', 'message',
    }

    def setUp(self):
        super().setUp()
        self.url = reverse('replenishment-founds')

        self.BertrandMeyer = user_models.User.create_new_user(
            email='bertrand@gmail.com',
            first_name='Bertrand',
            last_name='Meyer',
        )

    def test__successful_outcome(self):

        self.BertrandMeyer.wallet.increase_balance_on(Decimal('1'))

        data = {
            'amount': '500',
        }

        self.client.force_login(self.BertrandMeyer)

        resp = self.client.post(self.url, data)
        self.assertEqual(
            resp.status_code, status.HTTP_201_CREATED, resp.content,
        )
        self.assertSetEqual(set(resp.data), self.expected_fields)

        # Checks in DB:
        self.BertrandMeyer.wallet.refresh_from_db()
        self.assertEqual(self.BertrandMeyer.wallet.balance, Decimal('501'))


class TestWithdrawingFoundsEndpoint(test.APITestCase):
    """
    Testing an endpoint for withdrawing funds from the user account.
    """

    expected_fields = {
        'amount', 'transaction_id', 'created_at',
    }
    error_expected_fields = {
        'code', 'message',
    }

    def setUp(self):
        super().setUp()
        self.url = reverse('withdrawing-founds')

        self.EricEvans = user_models.User.create_new_user(
            email='ee@gmail.com',
            first_name='Eric',
            last_name='Evans',
        )

    def test__successful_outcome(self):

        self.EricEvans.wallet.increase_balance_on(Decimal('1000'))

        data = {
            'amount': '500.90',
        }

        self.client.force_login(self.EricEvans)

        resp = self.client.post(self.url, data)
        self.assertEqual(
            resp.status_code, status.HTTP_201_CREATED, resp.content,
        )
        self.assertSetEqual(set(resp.data), self.expected_fields)

        # Checks in DB:
        self.EricEvans.wallet.refresh_from_db()
        self.assertEqual(self.EricEvans.wallet.balance, Decimal('499.10'))

    def test_u2u_transfer__failed_cuz_not_enough_funds(self):
        self.EricEvans.wallet.increase_balance_on(Decimal('10'))

        data = {
            'amount': '15',
        }

        self.client.force_login(self.EricEvans)

        resp = self.client.post(self.url, data)
        self.assertEqual(
            resp.status_code, status.HTTP_400_BAD_REQUEST, resp.content,
        )
        data = resp.json()
        self.assertSetEqual(set(data), self.error_expected_fields)
        self.assertEqual(data['code'], 'invalid')
        self.assertEqual(data['message'], 'Insufficient funds')
