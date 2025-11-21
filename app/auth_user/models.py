from django.db import models
from app.core.models import AbstractModel
from django.contrib.auth.models import (
    AbstractBaseUser,
    Permission,
    BaseUserManager
)
from app.auth_user.constants import Account, Status, Gender

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
    

class QuixShareUser(AbstractBaseUser, AbstractModel):
    email = models.EmailField(unique=True, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    otp = models.IntegerField(null=True, blank=True)
    attempts_time = models.DateTimeField(null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = "email"

    class Meta:
        db_table = "quix_share_auth_user"


class QuixShareUserProfile(AbstractModel):
    user = models.OneToOneField(
        QuixShareUser,
        on_delete=models.PROTECT,
        related_name="quix_share_user_profile",
        null=True,
        blank=True
    )
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=25, choices=Gender.choices, default=Gender.OTHER)
    username = models.CharField(max_length=255, null=True, blank=True, unique=True)
    account_type = models.CharField(max_length=25, choices=Account.choices, default=Account.NORMAL)
    date_of_birth = models.DateField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=55, choices=Status.choices, default=Status.APPROVED)

    class Meta:
        db_table = "quix_share_user_profile"
