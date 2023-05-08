from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from .validators import CorrectUsernameValidator


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = [
        (ADMIN, 'ADMIN'),
        (MODERATOR, 'MODERATOR'),
        (USER, 'USER'),
    ]

    bio = models.TextField(max_length=settings.LENGTH_BIO, blank=True)
    role = models.CharField(max_length=settings.LENGTH_ROLE,
                            choices=ROLES, default='user')
    email = models.EmailField(max_length=settings.LENGTH_EMAIL, unique=True)
    username = models.CharField(unique=True,
                                max_length=settings.LENGTH_USERNAME,
                                validators=[UnicodeUsernameValidator(),
                                            CorrectUsernameValidator()])

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return (self.role == self.ADMIN
                or self.is_superuser)

    @property
    def is_moderator(self):
        return (self.role == self.MODERATOR
                or self.is_staff)
