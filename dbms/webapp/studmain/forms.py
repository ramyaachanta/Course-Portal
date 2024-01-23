from django import forms
from login.models import feedback,assignsub

class feedbackform(forms.ModelForm):
    class Meta:
        model=feedback
        fields=[
        'reg_no',
        'descp',
        ]

class assignsubform(forms.ModelForm):
    class Meta:
        model=assignsub
        fields=[
        'assignment_ans'
        ]