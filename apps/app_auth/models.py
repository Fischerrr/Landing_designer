from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

import logging

logger = logging.getLogger('django')


class Manager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError(u'Username is empty')

        user = self.model(email=email)
        user.set_password(password)
        user.is_active = True
        user.save()

        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save()


class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=200, unique=True, verbose_name='Логин')
    first_name = models.CharField(max_length=200, blank=True, verbose_name='Имя')
    last_name = models.CharField(max_length=200, blank=True, verbose_name='Фамилия')
    date_joined = models.DateTimeField(blank=True, null=True)

    is_staff = models.BooleanField('Доступ в админку', default=False, help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField('Активен', default=False, help_text='Designates whether this user should be treated as ''active. Unselect this instead of deleting accounts.')
    USERNAME_FIELD = 'email'

    objects = Manager()

    @property
    def username(self):
        """ backward compat with 3rd  extensions"""
        return self.email

    def get_short_name(self):
        return self.email if self.email else 'None'

    def get_full_name(self):
        if self.first_name and self.last_name:
            return '{} {}'.format(self.last_name, self.first_name)
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return self.email

    def __unicode__(self):
        return self.get_short_name()

    class Meta:
        app_label = 'app_auth'
        verbose_name = u'Пользователь'
        verbose_name_plural = u'Пользователи'
