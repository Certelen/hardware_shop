from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )


class UpdateUserForm(UserChangeForm):
    password1 = forms.CharField(
        label="Новый пароль",
        max_length=128,
        required=False
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        max_length=128,
        required=False
    )

    class Meta(UserChangeForm.Meta):
        model = User
        fields = (
            'first_name',
            'last_name',
            'birth_date',
            'phone',
            'username',
            'email',
            'password1',
            'password2',
        )

    def clean(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise ValidationError(
                'Пароль и его Подтверждение должны совпадать!')
