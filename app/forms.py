from django import forms
from django.forms import ValidationError
from django.contrib.auth import authenticate

from django import forms
from django.contrib.auth.models import User
from .models import User_profile

class RegistrationForm(forms.ModelForm):
    nickname = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=12)
    confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=8, max_length=12)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken. Please choose another.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 8 or len(password) > 12:
            raise ValidationError("Password must be between 8 and 12 characters.")
        return password

    def clean_confirm_password(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise ValidationError("Passwords do not match.")
        return confirm_password


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None or not user.check_password(password):
                raise ValidationError("Incorrect username or password")

        return cleaned_data

