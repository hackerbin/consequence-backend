from rest_framework import serializers

from truelayer.models import Bank, Card, Transaction, Merchant, Classification
from users.serializers import UserSerializer


class BankSerializer(serializers.ModelSerializer):
    # user = UserSerializer(write_only=True)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    # def user(self, obj):
    #     request = getattr(self.context, 'request', None)
    #     if request:
    #         return request.user

    class Meta:
        model = Bank
        fields = ['user', 'account_id', 'account_type', 'display_name', 'currency', 'account_number', 'provider',
                  'update_timestamp', 'created_at', 'updated_at']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }
    #
    # def to_representation(self, instance):
    #     ret = super().to_representation(instance)
    #     ret['user'] = UserSerializer(instance.user).data
    #     return ret


class CardSerializer(serializers.ModelSerializer):
    # user = UserSerializer(write_only=True)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    # def user(self, obj):
    #     request = getattr(self.context, 'request', None)
    #     if request:
    #         return request.user

    class Meta:
        model = Card
        fields = ['user', 'account_id', 'card_network', 'card_type', 'currency', 'display_name', 'partial_card_number',
                  'name_on_card', 'provider', 'update_timestamp', 'created_at', 'updated_at']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }


class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Merchant
        fields = ['title', 'co2e_factor', 'created_at', 'updated_at']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }


class ClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classification
        fields = ['category', 'subcategory', 'co2e_factor', 'created_at', 'updated_at']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }


class TransactionSerializer(serializers.ModelSerializer):
    # user = UserSerializer(write_only=True)
    transaction_classification = ClassificationSerializer(read_only=True)
    merchant_name = MerchantSerializer(read_only=True)

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    # def user(self, obj):
    #     request = getattr(self.context, 'request', None)
    #     if request:
    #         return request.user

    class Meta:
        model = Transaction
        depth = 1
        fields = ['user', 'account_type', 'account_id', 'timestamp', 'description', 'transaction_type',
                  'transaction_category', 'transaction_classification', 'merchant_name', 'amount', 'currency',
                  'transaction_id', 'running_balance', 'meta', 'created_at', 'updated_at']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def create(self, validated_data):
        transaction_classifications = self.initial_data['transaction_classification']
        merchant_name = self.initial_data['merchant_name']
        transaction = self.Meta.model.objects.create(**validated_data)
        if transaction_classifications:
            _category = transaction_classifications[0]
            _subcategory = transaction_classifications[1] if len(transaction_classifications) > 1 else ''
            _classification, _ = Classification.objects.get_or_create(category=_category, subcategory=_subcategory)
            transaction.transaction_classification = _classification
        if merchant_name:
            _merchant, _ = Merchant.objects.get_or_create(title=merchant_name)
            transaction.merchant_name = _merchant
        transaction.save()
        return transaction
