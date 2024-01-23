from django.contrib import admin

# Register your models here.
from .models import *
m=[User,Announcements,Faculty,assignment,materials,faq,feedback,assignsub,Course,Department,Student]
# ,assignment to do

admin.site.register(m)

