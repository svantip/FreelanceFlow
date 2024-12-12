from django import forms
from django.contrib.auth.hashers import make_password

from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        label="Username",
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your username'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Enter your password'})
    )


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(
        widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        # Ensure these fields match your User model
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        # Check if passwords match
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match!")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Hash the password before saving
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
