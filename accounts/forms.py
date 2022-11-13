from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User,Users,Roles
from datetime import date

this_year = date.today().year
# YEARS = [x for x in range(1950, 2050)]
YEARS = [x for x in range(this_year - 100, this_year + 1)]

class UserForm(forms.ModelForm):
   class Meta:
        model = Users
        fields = "__all__"
        widgets = {
               'name': forms.TextInput(attrs={'class': 'form-control form-control-user','placeholder': 'Full name', 'autocomplete':"off"},),
               'email': forms.EmailInput(attrs={'class': 'form-control form-control-user','placeholder': 'Email', 'autocomplete':"off"},),
               'address': forms.TextInput(attrs={'class': 'form-control form-control-user','placeholder': 'Address','autocomplete':"off"},),
               'dob':  forms.SelectDateWidget(attrs={'class': 'border-none'},years=YEARS),
               'contact_no': forms.TextInput(attrs={'class': 'form-control form-control-user','placeholder': 'Contact Number','autocomplete':"off"},),
               'password': forms.PasswordInput(attrs={'class': 'form-control form-control-user','placeholder': 'Password'},),
             # 'password2': forms.PasswordInput(attrs={'class': 'form-control form-control-user','placeholder': 'Repeat Password'},)
        }



