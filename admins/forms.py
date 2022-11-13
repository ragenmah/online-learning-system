from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from accounts.models import Roles,Courses

ROLES= [
    ('admin', 'Admin'),
    ('teacher', 'Teacher'),
    ('student', 'Student'),
    ]
#
# ROLES= [
#     ('1', 'Admin'),
#     ('2', 'Teacher'),
#     ('3', 'Student'),
#     ]

class RolesForm(forms.ModelForm):
    class Meta:
        model=Roles
        fields="__all__"
        widgets={
            'role_title':forms.Select(attrs={'class':'form-control'},choices=ROLES),
            'role_description':forms.Textarea(attrs={'class':'form-control'})
        }

class CourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields="__all__"