from django import forms

from accounts.models import Courses


class CourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        # fields="__all__"
        exclude = ('user_id',)
        widgets = {
            'course_title': forms.TextInput(attrs={'class': 'form-control', "placeholder": ""}),
            'course_description': forms.Textarea(attrs={'class': 'form-control', "placeholder": ""}),
            # 'course_thumbnail': forms.ImageField(attrs={'class': 'form-control'})
        }

