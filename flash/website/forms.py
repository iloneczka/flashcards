from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserChangeForm


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            print(user)
            if not user or not user.is_active:
                raise forms.ValidationError("Invalid username or password.")
        return cleaned_data


class GenerateTokenForm(forms.Form):
    generate_token = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        initial='Generate Token',
    )


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        fields = ('username',)
