import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
import pytz

from core.truelayer import TrueLayer
from core.utils import generate_random_float

utc = pytz.UTC


class User(AbstractUser):
    number_of_employee = models.IntegerField(null=True)
    email = models.EmailField(unique=True, null=False)

    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_truelayer_token(self):
        # Check if token exists
        if hasattr(self, 'truelayer_token'):
            # Check if token expired
            if self.truelayer_token.is_valid:
                return self.truelayer_token.access_token
            else:
                # refresh token
                truelayer = TrueLayer()
                token_object = truelayer.get_refresh_token(self.truelayer_token.refresh_token)
                if token_object:
                    self.truelayer_token.access_token = token_object['access_token']
                    self.truelayer_token.refresh_token = token_object['refresh_token']
                    self.truelayer_token.save()
                    # self.truelayer_token.__dict__.update(**token_object)
                    return token_object['access_token']
        return {}

    def tl_is_valid(self):
        return self.truelayer_token.is_valid()


class TruelayerToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name='truelayer_token')
    access_token = models.TextField()
    refresh_token = models.CharField(max_length=255)
    token_type = models.CharField(max_length=20)
    expires_in = models.IntegerField()
    scope = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_valid(self):
        if self.updated_at:
            if self.updated_at + datetime.timedelta(seconds=self.expires_in) > utc.localize(datetime.datetime.now()):
                return True
        else:
            if self.created_at + datetime.timedelta(seconds=self.expires_in) > utc.localize(datetime.datetime.now()):
                return True
        return False


class Business(models.Model):
    business_name = models.CharField(max_length=100, null=True, blank=True)
    nature_of_business = models.CharField(max_length=100, null=True, blank=True)
    user = models.ManyToManyField(
        User, related_name="business", through='UserBusiness')


class UserBusiness(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    business = models.ForeignKey(Business, on_delete=models.DO_NOTHING)
    number_of_employees = models.IntegerField()
    co2e_factor = models.FloatField(default=generate_random_float())

    class Meta:
        unique_together = (('user', 'business'),)
