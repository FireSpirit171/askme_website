from django import forms
from django.forms import ValidationError
from django.contrib.auth import authenticate
from app import models

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
                raise forms.ValidationError("Incorrect username or password")

        return cleaned_data

class RegistrationForm(forms.ModelForm):
    nickname = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    avatar = forms.ImageField()

    class Meta:
        model = models.User
        fields = ("username", "email", "password")
