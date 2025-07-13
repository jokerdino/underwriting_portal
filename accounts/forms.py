from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        ),
        label="",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        ),
        label="",
    )

    class Meta:
        model = get_user_model()
        fields = ["username", "password"]


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = [
            "oo_code",
            "user_type",
        ]


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = [
            "oo_code",
            "user_type",
            "reset_password",
        ]


class UploadExcelForm(forms.Form):
    file = forms.FileField()
