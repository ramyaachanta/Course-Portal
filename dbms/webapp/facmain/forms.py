from django import forms
from login.models import assignment,materials

class assignmentform(forms.ModelForm):
    class Meta:
        model=assignment
        fields=[
        'assignment_file',
        'marks',
        'message',
        ]

class materialsform(forms.ModelForm):
    class Meta:
        model=materials
        fields=[
        'lec_title',
        'lec_pdf',
        ]