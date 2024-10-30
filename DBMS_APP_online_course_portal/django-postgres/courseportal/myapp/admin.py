from django.contrib import admin

# Register your models here.
from .models import *
# ,assignment to do
m = [
    Department,
    Faculty,
    FacultyMobile,
    FacultyAnnouncements,
    FacultyAssignment,
    FacultyDepartment,
    FacultyMaterial,
    # FacultyFAQ,
    Student,
    StudentDepartment,
    StudentAnnouncements,
    StudentAssignmentSubmission,
    # StudentFAQ,
    StudentMobile,
    Feedback,
    AssignmentSubmission,
    Assignment,
    Course,
    Enrollment,
    Materials,
    FAQ,
    Announcements
]
admin.site.register(m)

