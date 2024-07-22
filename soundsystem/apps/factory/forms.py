from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Measure

from .models import *


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label="Логин",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password1 = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Повторите пароль",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label="Логин", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


class MeasureForm(forms.ModelForm):
    class Meta:
        model = Measure
        fields = ("measure_name", "data", "direct_start", "direct_stop")
        # fields = ('description', 'document', )

    def __init__(self, *args, **kwargs):
        super(MeasureForm, self).__init__(*args, **kwargs)
        # self.fields['author_name'].widget.attrs.update({'class': 'form-control'})
        self.fields["measure_name"].widget.attrs.update({"class": "form-control"})
        self.fields["direct_start"].widget.attrs.update({"class": "form-control"})
        self.fields["direct_stop"].widget.attrs.update({"class": "form-control"})
