from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    business_name = models.CharField(max_length=100, null=True, blank=True)
    business_nature = models.CharField(max_length=100, null=True, blank=True)
    number_of_employee = models.IntegerField(null=True)
    email = models.EmailField(unique=True, null=False)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
