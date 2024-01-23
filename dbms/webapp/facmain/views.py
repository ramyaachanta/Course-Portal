from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


from login.models import Announcements,Faculty,assignment,materials,faq,User,Course,assignsub
from django.shortcuts import render
from facmain.forms import assignmentform,materialsform
from facmain.functions import handle_upload_file






def facmain(request):
    a=Course.objects.all()
    return render(request,'facmain/fac_home.html',{'Course':a})
def facannouncement(request):
    ann=Announcements.objects.all()
    return render(request,'facmain/fac_ann.html',{'Announcements':ann})
def factest(request):
    
    return render(request,'facmain/fac_quiz.html')
def facprofile(request):
    facpro=Faculty.objects.all()[0]
    return render(request,'facmain/fac_profile.html',{'details':facpro})
def facgocourse(request):
    facpro=materials.objects.all()
    return render(request,'facmain/fac_course.html',{'materials':facpro})

def facsub(request):
    return render(request,'facmain/fac_assign.html')

def testdone(request):
    return render(request,'facmain/fac_course.html')

def assigndone(request):
    return render(request,'facmain/assigndone.html')

def matdone(request):
    return render(request,'facmain/matdonedone.html')

def ans(request):
    a=assignsub.objects.all()
    return render(request,'facmain/assignsubmitted.html',{'assignsub':a})

def facassigning(request):
    if request.method == 'POST':
        assign=assignmentform(request.POST,request.FILES)
        if assign.is_valid():
            #handle_upload_file(request.FILES['assignment_file'])
            model_instance=assign.save(commit=False)
            model_instance.save()
            return render(request,'facmain/assigndone.html')
    else:
        assign=assignmentform()
    return render(request,'facmain/fac_assign.html',{'form':assign})


def facassign(request):
    return render(request,'facmain/fac_assign.html')

def facfaq(request):
    a=faq.objects.all()
    return render(request,'facmain/fac_faq.html',{'faq':a})
    
def faccontact(request):
    return render(request,'facmain/fac_contact.html')
def facupload(request):
    if request.method == 'POST':
        mat=materialsform(request.POST,request.FILES)
        if mat.is_valid():
            #handle_upload_file(request.FILES['assignment_file'])
            model_instances=mat.save(commit=False)
            model_instances.save()
            return render(request,'facmain/matdone.html')
    else:
        mat=materialsform()
    return render(request,'facmain/fac_upload.html',{'form':mat})


def posting(request):
    value=request.POST

    subject='quiz link'
    message='please use this below link for test.LINK:"https://forms.office.com/Pages/ResponsePage.aspx?id=o835AF4H5USqC6ujrdZTn1ZzWpbksglCn4c6JT8KiTZURERMQUoxMjJCTzZKMkxKTk9MS1FUSTNSMy4u" ALL THE BEST!  Thank You!'
    from_email=settings.EMAIL_HOST_USER
    to_list=[settings.EMAIL_HOST_USER]
    send_mail(subject,message,from_email,to_list,fail_silently=True)
    return render(request,'facmain/testdone.html')
    