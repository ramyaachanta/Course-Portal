from django import forms

from myapp.models import Announcements, Assignment, AssignmentSubmission, Materials

# from myapp.models import AssignmentSubmission, Feedback

# class feedbackform(forms.ModelForm):
#     class Meta:
#         model=Feedback,
#         fields=[
#         'reg_no',
#         'descp',
#         ]

class assignsubform(forms.ModelForm):
    class Meta:
        model=AssignmentSubmission
        fields=[
        'message',
        'assignment_file_answer',
        'assignment_id',
        'reg_no'
        ]

class materialsform(forms.ModelForm):
    class Meta:
        model=Materials
        fields=[
        'material_file',
        'material_title',
        'description',
        'course_id'
        ]

class assignmentform(forms.ModelForm):
    class Meta:
        model=Assignment
        fields=[
        'total_marks',
        'message',
        'assignment_file_question',
        'end_time',
        'start_time',
        'title'
        ]
class announcementform(forms.ModelForm):
    class Meta:
        model=Announcements
        fields=[
        'publish_date',
        'description',
        'title'
        ]
