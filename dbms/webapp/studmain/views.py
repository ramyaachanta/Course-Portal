from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse

from login.models import Announcements,Student,faq,assignsub,assignment,Course,materials
from studmain.forms import feedbackform,assignsubform
from django.shortcuts import render

# Create your views here.
def assigndone(request):
    return render(request,'studmain/assigndone.html')
def quizdone(request):
    return render(request,'studmain/quizdone.html')
def feedone(request):
    return render(request,'studmain/feedone.html')

def studmain(request):
    #return HttpResponse("stud main")
    a=Course.objects.all()
    return render(request,'studmain/student page.html',{'Course':a})
def studannouncement(request):
    #return HttpResponse("announcement stud")
    ann=Announcements.objects.all()
    return render(request,'studmain/stud_ann.html',{'Announcements':ann})
def studtest(request):
    #return HttpResponse("test stud")
    return render(request,'studmain/stud_quiz_start.html')
def studprofile(request):
    #return render(request,'facmain/fac_quiz.html')
    
    studpro=Student.objects.all()[0]
    return render(request,'studmain/stud_profile.html',{'details':studpro})
def studgocourse(request):
    a=materials.objects.all()
    return render(request,'studmain/stud_module.html',{'materials':a})
def studfaq(request):
    a=faq.objects.all()
    return render(request,'studmain/stud_faq.html',{'faq':a})
def studcontact(request):
    return render(request,'studmain/stud_contact.html')
def studfeed(request):
    if request.method == 'POST':
        feed=feedbackform(request.POST)
        if feed.is_valid():
            #handle_upload_file(request.FILES['assignment_file'])
            model_instance=feed.save(commit=False)
            model_instance.save()
            return render(request,'studmain/feedone.html')
    else:
        feed=feedbackform()
    return render(request,'studmain/stud_feed.html',{'form':feed})
def studpro(request):
    if request.method == "POST":
        assignsub=assignsubform(request.POST,request.FILES)
        if assignsub.is_valid():
            m=assignsub.save(commit=False)
            m.save()
            return render(request,'studmain/assigndone.html')
    else:
        assignsub=assignsubform()
    return render(request,'studmain/studpro.html',{'form':assignsub})
def studassignsub(request):
    m=assignment.objects.all()[0]
    assignsub=assignsubform()
    return render(request,'studmain/stud_assign_sub.html',{'a':m,'form':assignsub})

def submitted(request):
    return HttpResponse('your in the ')
  

def studmodule(request):
    return render(request,'studmain/stud_module.html')

def studgrade(request):
    return render(request,'studmain/stud_grades.html')

def studreg(request):
    a=Course.objects.all()
    return render(request,'studmain/stud_reg.html',{'Course':a})