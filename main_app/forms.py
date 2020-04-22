from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_select2 import forms as s2forms
from multiselectfield import MultiSelectField
from . models import Customer, Volunteer, TIMESLOTS



class CustomerSignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')
    delivery_time = MultiSelectField(
        max_length=100, null=True, choices=TIMESLOTS, max_choices=3)


class VolunteerSignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')
    availability_date = forms.DateField()
    availability = forms.MultipleChoiceField(choices=TIMESLOTS)
    # availability = forms.MultipleChoiceField(choices=TIMESLOTS, widget=s2forms.Select2MultipleWidget)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',
                  'password1', 'password2', 'availability_date', 'availability')
