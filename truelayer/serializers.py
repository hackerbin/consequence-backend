from rest_framework import serializers

from truelayer.models import Bank


class BankSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('_user')

    def _user(self, obj):
        request = getattr(self.context, 'request', None)
        if request:
            return request.user

    class Meta:
        model = Bank
        fields = ['user', 'account_id', 'account_type', 'display_name', 'currency', 'account_number', 'provider',
                  'update_timestamp', 'created_at', 'updated_at']
        extra_kwargs = {
            'user': {'write_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True}
        }
