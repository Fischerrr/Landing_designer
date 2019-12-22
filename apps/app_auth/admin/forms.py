from __future__ import unicode_literals
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from apps.app_auth.models import AppUser
from django import forms


class AppCreationUserForm(UserCreationForm):
    email = forms.EmailField(label='Эл. почта')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            AppUser._default_manager.get(email=email)
        except AppUser.DoesNotExist:
            return email
        raise forms.ValidationError(
            'Пользователь уже существует',
            code='duplicate_email',
        )

    class Meta:
        model = AppUser
        fields = ('email',)


class AppChangeUserForm(UserChangeForm):
    class Meta:
        model = AppUser
        fields = '__all__'
