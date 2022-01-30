from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from myapp.models import Item, ItemShare

User = get_user_model()


class AccountSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class ItemShareSerializer(ModelSerializer):

    class Meta:
        model = ItemShare
        fields = "__all__"
