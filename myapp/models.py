from django.contrib.auth.models import AbstractUser
from django.db import models

from Account import settings


class UserAccount(AbstractUser):
    pass


class Item(models.Model):
    """
    This model is used to store user items.
    """

    created_by = models.ForeignKey(UserAccount, on_delete=models.CASCADE, editable=False, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=settings.MEDIA_ROOT, null=True, blank=True)


class ItemShare(models.Model):
    """
    This model is used to store shared item and user.
    """

    ACCESS_TYPE = (("V", "VIEW"), ("E", "EDIT"))
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    shared_to = models.ForeignKey(UserAccount, on_delete=models.CASCADE, blank=True, null=True)
    access_type = models.CharField(max_length=4, choices=ACCESS_TYPE, default="V")


