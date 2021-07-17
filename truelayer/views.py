import json

from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config import constants
from config.constants import BANK, CARD
from core.truelayer import TrueLayer
from truelayer.models import Bank, Card, Transaction, Classification, Merchant
from truelayer.serializers import BankSerializer, CardSerializer, TransactionSerializer
from users.models import TruelayerToken


class CallbackAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        code = request.data.get('code', None)
        truelayer = TrueLayer()
        token_object = truelayer.connect(code)
        if token_object:
            user = request.user
            if hasattr(user, 'truelayer_token'):
                # user.truelayer_token.__dict__.update(**token_object)  # Need to fix
                user.truelayer_token.access_token = token_object['access_token']
                user.truelayer_token.refresh_token = token_object['refresh_token']
                user.truelayer_token.save()
            else:
                token_object['user'] = user
                TruelayerToken.objects.create(**token_object)
            return Response({'message': 'Account Linked'})
        else:
            raise AuthenticationFailed('Invalid Code')


class BanksAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        truelayer = TrueLayer()
        truelayer.set_access_token(request.user.get_truelayer_token())
        all_accounts = truelayer.list_all_bank_accounts()
        return Response(all_accounts)


class CardsAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        truelayer = TrueLayer()
        truelayer.set_access_token(request.user.get_truelayer_token())
        all_cards = truelayer.list_all_cards()
        return Response(all_cards)


class LinkAccount(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        # only for development
        Bank.objects.all().delete()
        Card.objects.all().delete()
        Transaction.objects.all().delete()
        Classification.objects.all().delete()
        Merchant.objects.all().delete()
        # only for development end

        account_id = request.data.get('account_id', None)
        account_type = request.data.get('account_type', None)  # bank/card
        if account_id and account_type:
            if account_type == BANK:
                truelayer = TrueLayer()
                truelayer.set_access_token(request.user.get_truelayer_token())
                bank_account = truelayer.retrieve_bank_account(account_id)
                if "results" in bank_account and bank_account["results"]:
                    # Link Bank
                    bank_obj = bank_account["results"][0]
                    bank_obj['user'] = request.user
                    serializer = BankSerializer(data=bank_obj, context={
                        'request': request
                    })
                    serializer.is_valid(raise_exception=True)
                    serializer.save()

                    # Link Bank Transaction
                    transactions = truelayer.retrieve_bank_account_transactions(account_id)
                    if "results" in transactions and transactions["results"]:
                        for transaction in transactions["results"]:
                            # transaction['user'] = request.user.pk
                            transaction['account_type'] = constants.BANK
                            transaction['account_id'] = bank_obj['account_id']
                            if not "merchant_name" in transaction:
                                transaction['merchant_name'] = ""
                            transaction_serializer = TransactionSerializer(data=transaction, context={
                                'request': request
                            })
                            transaction_serializer.is_valid(raise_exception=True)
                            transaction_serializer.save()

                    return Response(serializer.data)
            elif account_type == CARD:
                truelayer = TrueLayer()
                truelayer.set_access_token(request.user.get_truelayer_token())
                card_account = truelayer.retrieve_card(account_id)
                if "results" in card_account and card_account["results"]:
                    card_obj = card_account["results"][0]
                    card_obj['user'] = request.user.pk
                    serializer = CardSerializer(data=card_obj)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    return Response(serializer.data)
        raise ValidationError('Invalid account info')


class GetAccount(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        account_id = request.data.get('account_id', None)
        account_type = request.data.get('account_type', None)  # bank/card
        if account_id and account_type:
            if account_type == BANK:
                truelayer = TrueLayer()
                truelayer.set_access_token(request.user.get_truelayer_token())
                bank_account = truelayer.retrieve_bank_account(account_id)
                return Response(bank_account)
            elif account_type == CARD:
                truelayer = TrueLayer()
                truelayer.set_access_token(request.user.get_truelayer_token())
                card_account = truelayer.retrieve_card(account_id)
                return Response(card_account)
        raise ValidationError('Invalid account info')


class GetLinkedAccounts(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        banks = Bank.objects.filter(user=request.user)
        cards = Card.objects.filter(user=request.user)
        bank_serializer = BankSerializer(banks, many=True)
        card_serializer = CardSerializer(cards, many=True)
        return Response({'banks': bank_serializer.data, 'cards': card_serializer.data})


class GetLinkedTransactions(APIView):
    def get(self, request):
        transactions = Transaction.objects.filter(user=request.user)
        transaction_serializer = TransactionSerializer(transactions, many=True)
        return Response(transaction_serializer.data)
