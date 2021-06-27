import uuid
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from accounts.managers import CustomUserManager

class User(AbstractBaseUser, PermissionsMixin):

    # ROLES
    ADMIN = "admin"
    INPUT = "input"
    LOOK = "look"

    ROLE_CHOICES = (
        (ADMIN, "Admin"),
        (INPUT, "input"),
        (LOOK, "look")
    )

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    # FIELDS
    # uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4(), verbose_name='Public Identifier')
    username = models.TextField(unique=True)
    role = models.TextField(choices=ROLE_CHOICES, default="look")
    salary = models.PositiveBigIntegerField(null=True)
    created_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(_('staff status'), default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username

