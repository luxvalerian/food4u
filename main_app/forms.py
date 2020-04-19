from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from . models import Customer, Volunteer


class CustomerSignUpForm(UserCreationForm):
  first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
  last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
  email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')

class VolunteerSignUpForm(UserCreationForm):
  first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
  last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
  email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

  class Meta:
    model = User
    fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')