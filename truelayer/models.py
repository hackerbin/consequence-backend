from django.db.models import JSONField, Q
from django.db import models

from config.constants import ACCOUNT_TYPE_CHOICE
from core.utils import generate_random_float
from users.models import User


class Bank(models.Model):
    """
    'update_timestamp': '2021-07-05T18:09:01.0581797Z',
     'account_id': '56c7b029e0f8ec5a2334fb0ffc2fface',
     'account_type': 'TRANSACTION',
     'display_name': 'TRANSACTION ACCOUNT 1',
     'currency': 'GBP',
     'account_number': {'swift_bic': 'CPBKGB00',
                            'number': '10000000',
                        'sort_code': '01-21-31'},
     'provider': {'display_name': 'MOCK',
                      'provider_id': 'mock',
              'logo_uri': 'https://truelayer-client-logos.s3-eu-west-1.amazonaws.com/banks/banks-icons/mock-icon.svg'}}
    """
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='banks')
    account_id = models.CharField(max_length=64, unique=True)
    account_type = models.CharField(max_length=64)
    display_name = models.CharField(max_length=255)
    currency = models.CharField(max_length=10)
    account_number = JSONField()
    provider = JSONField()
    update_timestamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.account_id

    @staticmethod
    def create_from_object(obj, user):
        obj['user'] = user
        _created_obj = Bank.objects.create(**obj)
        return _created_obj


class Card(models.Model):
    """
    {'account_id': '2cbf9b6063102763ccbe3ea62f1b3e72',
                      'card_network': 'MASTERCARD',
                      'card_type': 'CREDIT',
                      'currency': 'GBP',
                      'display_name': 'CREDIT CARD 1',
                      'partial_card_number': '1000',
                      'name_on_card': 'John Doe ',
                      'update_timestamp': '2021-07-05T18:09:18.1906563Z',
                      'provider': {'display_name': 'MOCK',
                                   'provider_id': 'mock',
                                   'logo_uri': 'https://truelayer-client-logos.s3-eu-west-1.amazonaws.com/banks/banks-icons/mock-icon.svg'}}
    """
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='cards')
    account_id = models.CharField(max_length=64, unique=True)
    card_network = models.CharField(max_length=64)
    card_type = models.CharField(max_length=64)
    currency = models.CharField(max_length=10)
    display_name = models.CharField(max_length=255)
    partial_card_number = models.CharField(max_length=64)
    name_on_card = models.CharField(max_length=255)
    provider = JSONField()
    update_timestamp = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.account_id


class Classification(models.Model):
    category = models.CharField(max_length=255)
    subcategory = models.CharField(max_length=255, null=True)
    co2e_factor = models.FloatField(default=generate_random_float())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('category', 'subcategory',)

    def __str__(self):
        return self.title


class Merchant(models.Model):
    title = models.CharField(max_length=255, unique=True)
    co2e_factor = models.FloatField(default=generate_random_float())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Transaction(models.Model):
    """
    'timestamp': '2021-07-05T00:00:00Z',
      'description': 'LNK ATM WITHDRAWAL',
      'transaction_type': 'DEBIT',
      'transaction_category': 'ATM',
      'transaction_classification': [],
      'amount': -60.0,
      'currency': 'GBP',
      'transaction_id': '2235c2ba8d700ce39e0c69cef3c7fe61',
      'running_balance': {'currency': 'GBP', 'amount': 594.87},
      'meta': {'provider_transaction_category': 'CPT'}},
    """
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='transactions')
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICE)
    account_id = models.CharField(max_length=64)  # card transaction id

    timestamp = models.DateTimeField()
    description = models.CharField(max_length=255)
    transaction_type = models.CharField(max_length=64)
    transaction_category = models.CharField(max_length=64)
    transaction_classification = models.ForeignKey(Classification, on_delete=models.DO_NOTHING, related_name='transactions', null=True)
    merchant_name = models.ForeignKey(Merchant, on_delete=models.DO_NOTHING, related_name='transactions', null=True)
    amount = models.FloatField()
    currency = models.CharField(max_length=10)
    transaction_id = models.CharField(max_length=64)
    running_balance = JSONField()
    meta = JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account_id} - {self.account_type} - {self.transaction_id}"

    def get_impact(self):
        if self.merchant_name:
            impact = self.amount * self.merchant_name.co2e_factor
        elif self.transaction_classification:
            impact = self.amount * self.transaction_classification.co2e_factor
        else:
            impact = self.amount

        return impact


    @staticmethod
    def get_avarage_impact():
        Transaction.objects.filter(Q(transaction_classification__isnull=False) | Q(merchant_name__isnull=False))