from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'date_of_birth', 'profile_photo')


class ExampleForm(forms.Form):
    example_field = forms.CharField(max_length=100)
