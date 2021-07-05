import json

from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from config.constants import BANK, CARD
from core.truelayer import TrueLayer
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
                user.truelayer_token.__dict__.update(**token_object)
            else:
                token_object['user'] = user
                TruelayerToken.objects.create(**token_object)
            return Response({'message': 'Account Linked'})
        else:
            raise AuthenticationFailed('Invalid Code')


class BanksAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        truelayer = TrueLayer()
        truelayer.set_access_token(request.user.get_truelayer_token())
        all_accounts = truelayer.list_all_accounts()
        return Response(all_accounts)


class CardsAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        truelayer = TrueLayer()
        truelayer.set_access_token(request.user.get_truelayer_token())
        all_cards = truelayer.list_all_cards()
        return Response(all_cards)


class LinkAccount(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        account_id = request.data.get('account_id', None)
        account_type = request.data.get('account_type', None)  # bank/card
        if account_id and account_type:
            if account_type == BANK:
                truelayer = TrueLayer()
                truelayer.set_access_token(request.user.get_truelayer_token())
                bank_account = truelayer.retrieve_bank_account(account_id)
                # TODO: check and add to model
                # TODO: Response
            elif account_type == CARD:
                truelayer = TrueLayer()
                truelayer.set_access_token(request.user.get_truelayer_token())
                card_account = truelayer.retrieve_card(account_id)
                # TODO: check and add to model
                # TODO: Response
        raise ValidationError('Invalid account info')
