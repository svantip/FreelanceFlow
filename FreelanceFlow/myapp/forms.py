from django import forms
from django.contrib.auth.hashers import make_password

from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Username'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Password'
            }
        )
    )


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Username'
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Email'
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Password'
            }
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'block w-full rounded-lg border-gray-300 shadow-sm p-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Confirm Password'
            }
        )
    )

    class Meta:
        model = User
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
