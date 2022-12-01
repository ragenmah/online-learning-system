from django import forms
from .models import Users, ChangePassword
from datetime import date

this_year = date.today().year
# YEARS = [x for x in range(1950, 2050)]
YEARS = [x for x in range(this_year - 100, this_year + 1)]


class UserForm(forms.ModelForm):
   class Meta:
        model = Users
        fields = "__all__"
        exclude = ('profile_image', 'profile_description', 'current_position')
        widgets = {
               'name': forms.TextInput(attrs={'class': 'form-control form-control-user','placeholder': 'Full name', 'autocomplete':"off"},),
               'email': forms.EmailInput(attrs={'class': 'form-control form-control-user','placeholder': 'Email', 'autocomplete':"off"},),
               'address': forms.TextInput(attrs={'class': 'form-control form-control-user','placeholder': 'Address','autocomplete':"off"},),
               'dob':  forms.SelectDateWidget(attrs={'class': 'form-control snps-inline-select border-none', 'data-date-format': 'dd/mm/yyyy',},years=YEARS),
               'contact_no': forms.TextInput(attrs={'class': 'form-control form-control-user','placeholder': 'Contact Number','autocomplete':"off"},),
               'password': forms.PasswordInput(attrs={'class': 'form-control form-control-user','placeholder': 'Password'},),
             # 'password2': forms.PasswordInput(attrs={'class': 'form-control form-control-user','placeholder': 'Repeat Password'},)
        }


class UserEditForm(forms.ModelForm):
    class Meta:
        model = Users
        exclude = ('user_role_id', 'password')
        widgets = {
                    'profile_description': forms.Textarea(attrs={'class': 'form-control', "placeholder": ""}),
                     'current_position': forms.TextInput(attrs={'class': 'form-control form-control-user', 'placeholder': ''}, ),
        }


class ChangePasswordForm(forms.ModelForm):
    class Meta:
        model = ChangePassword
        fields="__all__"
        widgets = {
            'old_password': forms.PasswordInput(attrs={'class': 'form-control form-control-user','placeholder': '******'},),
            'new_password': forms.PasswordInput(attrs={'class': 'form-control form-control-user','placeholder': '******'},),
            'retype_password': forms.PasswordInput(attrs={'class': 'form-control form-control-user','placeholder': '******'},),
        }

