from rest_framework import serializers

from users.models import User, NatureOfBusiness, Business


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'business']
        extra_kwargs = {
            'password': {'write_only': True},
            'id': {'read_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance


class NatureOfBusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = NatureOfBusiness
        fields = ['id', 'title', 'impact_per_member']
        extra_kwargs = {
            'id': {'read_only': True},
            'title': {'read_only': True},
            'impact_per_member': {'read_only': True}
        }


class BusinessSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nature_of_business = serializers.PrimaryKeyRelatedField(queryset=NatureOfBusiness.objects.all(), required=True,
                                                            allow_null=False)

    class Meta:
        model = Business
        depth = 1
        fields = ['id', 'user', 'business_name', 'number_of_employees', 'nature_of_business']
        extra_kwargs = {
            'id': {'read_only': True},
            # 'nature_of_business': {'read_only': True}
        }

    def create(self, validated_data):
        business = self.Meta.model.objects.create(**validated_data)
        return business


class BusinessGetSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nature_of_business = NatureOfBusinessSerializer()

    class Meta:
        model = Business
        depth = 1
        fields = ['id', 'user', 'business_name', 'number_of_employees', 'nature_of_business']
        extra_kwargs = {
            'id': {'read_only': True},
            'nature_of_business': {'read_only': True}
        }


class UserSerializer(serializers.ModelSerializer):
    business = BusinessGetSerializer()

    class Meta:
        model = User
        depth = 1
        fields = ['id', 'email', 'business']
        extra_kwargs = {
            'id': {'read_only': True}
        }
