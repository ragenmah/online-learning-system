from django import forms

from accounts.models import Courses, Resources, Tests, Fees


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


class CourseResourceForm(forms.ModelForm):
    class Meta:
        model = Resources
        # fields="__all__"
        exclude = ('course_id','resource_type')
        widgets = {
            'resource_title': forms.TextInput(attrs={'class': 'form-control', "placeholder": ""}),
            'resource_description': forms.Textarea(attrs={'class': 'form-control', "placeholder": ""}),
        }


class CourseQuestionForm(forms.ModelForm):
    class Meta:
        model = Tests
        # fields="__all__"
        exclude = ('course_id',)
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control', "placeholder": ""}),
            'option1': forms.TextInput(attrs={'class': 'form-control', "placeholder": ""}),
            'option2': forms.TextInput(attrs={'class': 'form-control', "placeholder": ""}),
            'option3': forms.TextInput(attrs={'class': 'form-control', "placeholder": ""}),
            'option4': forms.TextInput(attrs={'class': 'form-control', "placeholder": ""}),
            'option5': forms.TextInput(attrs={'class': 'form-control', "placeholder": ""}),
        }


class FeesForm(forms.ModelForm):
    class Meta:
        model = Fees
        exclude = ('course_id',)
        widgets = {
            'price': forms.NumberInput(attrs={'class': 'form-control', "placeholder": ""}),
            'discount_percentage': forms.NumberInput(attrs={'class': 'form-control', "placeholder": ""}),
            'discount_amount': forms.TextInput(attrs={'class': 'form-control', "placeholder": ""}),
        }



