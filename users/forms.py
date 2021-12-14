from django.contrib.auth import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(help_text="Enter a valid email address")


    class meta:
        model = User


        fields = ["username", 'email', "password1", "password2"]

        