from django.db import transaction
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from myapp.models import UserAccount, Item, ItemShare
from myapp.serializers import AccountSerializer, ItemSerializer, ItemShareSerializer
from django.contrib.auth.password_validation import validate_password


class AccountViewSet(viewsets.ModelViewSet):
    """
    This api is used to do account CRUD operations
    """

    queryset = UserAccount.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [
        permissions.AllowAny
    ]

    @transaction.atomic
    @action(methods=["POST"], detail=False, url_path="update-password", url_name="update-password")
    def update_password(self, request):
        """
        This api is used to update user password. Login user can only update password.
        Sample Post Data:
        {
            "old_password": "old@password",
            "new_password": "new@password"
        }
        """

        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        user = request.user
        if not user.is_authenticated:
            raise ValidationError("Authenticated user can only update password")

        if user.check_password(old_password):
            try:
                validate_password(new_password)
            except Exception as error:
                raise ValidationError("Invalid password :" + str(error))
            user.set_password(new_password)
            user.save()
        else:
            raise ValidationError("Old password are not correct")
        return Response({"message": "Password updated successfully"})


class ItemViewSet(viewsets.ModelViewSet):
    """
    This api is used to do user item CRUD operations
    """

    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    @transaction.atomic
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if request.user not in [instance.created_by] + list(UserAccount.objects.filter(itemshare=instance,
                                                                                   itemshare__access_type="E")):
            raise ValidationError("Access denied.")
        return super(ItemViewSet, self).update(request, *args, **kwargs)


class ItemShareViewSet(viewsets.ModelViewSet):
    """
    This api is used to do item share CRUD operations
    """

    queryset = ItemShare.objects.all()
    serializer_class = ItemShareSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        item = request.data.get("item")
        item = Item.objects.get(id=item)
        if request.user not in [item.created_by] + list(UserAccount.objects.filter(
                itemshare__item=item, itemshare__access_type="E")):
            raise ValidationError("Access denied.")

        return super(ItemShareViewSet, self).create(request, *args, **kwargs)

