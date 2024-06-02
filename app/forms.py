from django import forms
from django.forms import ValidationError
from django.contrib.auth import authenticate

from django import forms
from django.contrib.auth.models import User
from .models import User_profile

import re

class RegistrationForm(forms.ModelForm):
    nickname = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
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
        self.cleaned_data['validated_password'] = password
        if len(password) < 8 or len(password) > 12:
            raise ValidationError("Password must be between 8 and 12 characters.")
        if not re.match(r'^[a-zA-Z0-9]+$', password):
            raise ValidationError("Password must contain only latin letters and numbers.")
        return password

    def clean_confirm_password(self):
        password = self.cleaned_data.get("validated_password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise ValidationError("Passwords do not match.")
        return confirm_password
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


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

class SettingsForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.CharField()

    class Meta:
        model = User_profile
        fields = ['nickname', 'avatar']

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if User.objects.exclude(pk=self.instance.user_id).filter(username=username).exists():
            raise ValidationError('Editing error. This username is already taken.')

        if User.objects.exclude(pk=self.instance.user_id).filter(email=email).exists():
            raise ValidationError('Editing error. This email is already registered.')

        return cleaned_data