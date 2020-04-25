from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django_select2 import forms as s2forms
from multiselectfield import MultiSelectField
from . models import Customer, Volunteer, TIMESLOTS

class EditCustomerForm(UserChangeForm):
    
    class Meta:
        model = User

        fields = ('email', 'first_name', 'last_name', 'username')
        eclude = ('password')

class EditVolunteerForm(UserChangeForm):
    availability_date = forms.DateField()
    availability = forms.MultipleChoiceField(choices=TIMESLOTS)
    
    class Meta:
        model = User

        fields = ('email', 'first_name', 'last_name', 'username', 'availability_date', 'availability')
        eclude = ('password')

class EditVolunteerAvailablityForm(UserChangeForm):
    
    class Meta:
        model = Volunteer

        fields = ('availability_date', 'availability')

class CustomerUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')
    username = forms.CharField(
        max_length=254, help_text='Required. Inform a valid username.')

    class Meta:
        model = Customer
        fields = ('first_name', 'last_name', 'username', 'email')


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class CustomerSignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(
        max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(
        max_length=254, help_text='Required. Inform a valid email address.')
    # delivery_time = forms.MultipleChoiceField(choices=TIMESLOTS, widget=s2forms.Select2MultipleWidget)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',
                  'password1', 'password2')


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
