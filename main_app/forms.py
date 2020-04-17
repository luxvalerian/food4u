from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer, User

class CustomerSignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=200)
    first_name = forms.CharField(max_length=60)
    last_name = forms.CharField(max_length=60)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')

    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        customer = Customer.objects.create(user=user)
        return user

class VolunteerSignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=200)
    first_name = forms.CharField(max_length=60)
    last_name = forms.CharField(max_length=60)
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_volunteer = True
        if commit:
          user.save()
        return user