from django.conf import settings
from django.forms import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse  # Import the messages framework
from django.db.models import Count

from myapp.forms import announcementform, assignmentform, assignsubform, materialsform
from myapp.models import FAQ, Announcements, Assignment, AssignmentSubmission, Course, Enrollment, Faculty, FacultyAnnouncements, FacultyAssignment, FacultyDepartment, FacultyMaterial, FacultyMobile, Materials,Student, StudentAssignmentSubmission,StudentMobile,StudentDepartment

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        utype = request.POST.get('type')
        if utype == 'faculty':
            # Query the Faculty model to check if the credentials are correct
            try:
                fac = Faculty.objects.get(fac_id=username, password=password)
                request.session['faculty'] = {'fac_id':fac.fac_id}
                return redirect('/facmain/')  # Render the 'facmain.html' template with the faculty object
            except Faculty.DoesNotExist:
                return render(request, 'login/error.html')
        elif utype == 'student':
            # Query the Student model to check if the credentials are correct
            try:
                stud = Student.objects.get(reg_no=username, password=password)
                request.session['student'] = {'reg_no': stud.reg_no}  # Add more fields as needed
                return redirect('/studmain/')  # Redirect student users to the studmain page

               # Return a simple welcome message
            except Student.DoesNotExist:
                return render(request, 'login/error.html')
        else:
            return render(request, 'login/error.html')  # Handle unknown user types
    else:
        return render(request, 'login/login.html')

def home(request):
    return render(request, 'login/home.html')

def doLogout(request):
    # Clear all session keys
    k=request.session.get('student')
    for key in list(request.session.keys()):
        del request.session[key]

    # Redirect based on user type
    if k:
        return redirect('/login/?name=login&type=student')
    else:
        return redirect('/login/?name=login&type=faculty')


def forgot_password(request):
    if request.method == 'POST':
        # email = request.POST.get('email')
        # # Perform logic to check if email exists in your database
        # # If email exists, generate a password reset link and send it via email
        # # Example:
        # send_mail(
        #     'Password Reset',
        #     'Click the link to reset your password: <a href="...">Reset Password</a>',
        #     'from@example.com',
        #     [email],
        #     fail_silently=False,
        # )
        # Display a message indicating that the password reset email has been sent
        return render(request, 'login/forgot_password_success.html')
    return render(request, 'login/forgot_password.html')

def studmain(request):
    student = request.session.get('student')
    stud_enrollments = Enrollment.objects.filter(reg_no=student['reg_no'])
    courses_info = []

    for enrollment in stud_enrollments:
        course_details = {}
        course = Course.objects.get(course_id=enrollment.course_id_id)  # Retrieve course details
        fac_name = Faculty.objects.get(fac_id=enrollment.fac_id_id)  # Retrieve faculty name
        course_details['course_name'] = course.course_name
        course_details['course_credits'] = course.credits
        course_details['department'] = course.department_name.department_name
        course_details['course_img'] = course.course_img
        course_details['course_id'] = course.course_id
        course_details['fac_id'] = enrollment.fac_id_id
        course_details['fac_name'] = fac_name.first_name  # Assuming first_name holds the faculty name
        # Add more details as needed
        courses_info.append(course_details)

    print(course_details)
    return render(request, 'studmain/student_page.html', {'Course': courses_info})

def studprofile(request):    
    student_info = request.session.get('student')
    stud = Student.objects.get(reg_no=student_info['reg_no'])
    stud_dept=StudentDepartment.objects.get(reg_no=student_info['reg_no'])
    stud_mobile = StudentMobile.objects.filter(reg_no=student_info['reg_no']).first()
    student = {'reg_no': stud.reg_no,'email':stud.email,'name':stud.first_name,'department':stud_dept.department_name.department_name,'mobile':stud_mobile.mobile_no,'gender':stud.gender}  # Add more fields as needed
    return render(request,'studmain/stud_profile.html',{'details':student})

def studDoProfile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        reg_no = request.POST.get('reg_no')
        mobile = request.POST.get('mobile')
        student = Student.objects.get(reg_no=reg_no)
        try:
            student = Student.objects.get(reg_no=reg_no)
        except Student.DoesNotExist:
            error_message = "Student does not exist"
            return HttpResponse(error_message)
        student.first_name = name
        student.email = email
        if gender=="male":
            student.gender = "M"
        else:
            student.gender="F"

        student.save()
        try:
            student_mobile = StudentMobile.objects.get(reg_no=reg_no)
            student_mobile.mobile_no = mobile

            student_mobile.save()
        except StudentMobile.DoesNotExist:

            StudentMobile.objects.create(reg_no=reg_no, mobile_no=mobile)
        messages.success(request, 'Profile updated successfully.')

        # Redirect to a success page or render the profile page again with updated details
        return redirect('/studprofile/')  # Assuming you have a URL named 'profile' for rendering the profile page
    else:
        # If the request method is not POST, redirect to some error page or handle it accordingly
        error_message = "Invalid request method"
        return HttpResponse(error_message)


def studreg(request):
    # a=Course.objects.all()
    student = request.session.get('student')
    stud_courses = Enrollment.objects.filter(reg_no=student['reg_no'])
    courses_info = []
    course_ids = [stud_course.course_id for stud_course in stud_courses]
    for stud_course in course_ids:
        course_details = {}
        course = Course.objects.get(course_id=stud_course.course_id)  # Changed filter to get
        course_details['course_name'] = course.course_name
        course_details['course_credits'] = course.credits
        course_details['department'] = course.department_name
        course_details['course_id']=course.course_id
        course_details['course_type']=course.course_type
        #must write status
        # Add more details as needed
        courses_info.append(course_details)
    return render(request,'studmain/stud_reg.html',{'Course':courses_info})



    
def assigndone(request):
    return render(request,'studmain/assigndone.html')
def quizdone(request):
    return render(request,'studmain/quizdone.html')
def feedone(request):
    return render(request,'studmain/feedone.html')

def studgradelist(request):
    #return HttpResponse("test stud")
    stud_info = request.session.get('student')
    course_id = request.GET.get('course_id')
    fac_id = request.GET.get('fac_id')
    course = Course.objects.get(course_id=course_id)
    fac_ass_ids = FacultyAssignment.objects.filter(fac_id=fac_id, course_id=course_id).values_list('assignment_id', flat=True)
    
    # Filter assignments related to the current course and faculty
    assignments = Assignment.objects.filter(assignment_id__in=fac_ass_ids)
    student_instance = Student.objects.get(reg_no=stud_info['reg_no'])
    
    marks_list = []
    for assignment in assignments:
        try:
            student_assignment = StudentAssignmentSubmission.objects.get(reg_no=student_instance, assignment_id=assignment)
            marks_list.append(student_assignment.marks)
        except StudentAssignmentSubmission.DoesNotExist:
            marks_list.append(None)
    
    # Pass data to the template and render it
    context = {
        'assignments': zip(assignments, marks_list),
        'fac_id': fac_id,
        'course': course,
    }

    return render(request,'studmain/stud_grade_list.html',context)

def studgocourse(request):
    course_id = request.GET.get('course_id')
    fac_id=request.GET.get('fac_id')
    course = Course.objects.get(course_id=course_id)
    fac_mat_ids = FacultyMaterial.objects.filter(fac_id=fac_id).values_list('material_id', flat=True)
    faculty_materials = Materials.objects.filter(course_id=course_id, material_id__in=fac_mat_ids)

    course_details = {
        'course_name': course.course_name,
        'course_id':course.course_id,
        'materials': faculty_materials,
        'fac_id':fac_id,
    }

    return render(request, 'studmain/stud_module.html', {'course_details': course_details})

def studassignment(request):
    # Retrieve relevant data
    stud_info = request.session.get('student')
    course_id = request.GET.get('course_id')
    fac_id = request.GET.get('fac_id')
    course = Course.objects.get(course_id=course_id)
    fac_ass_ids = FacultyAssignment.objects.filter(fac_id=fac_id, course_id=course_id).values_list('assignment_id', flat=True)
    
    # Filter assignments related to the current course and faculty
    assignments = Assignment.objects.filter(assignment_id__in=fac_ass_ids)
    student_instance = Student.objects.get(reg_no=stud_info['reg_no'])
    
    marks_list = []
    for assignment in assignments:
        try:
            student_assignment = StudentAssignmentSubmission.objects.get(reg_no=student_instance, assignment_id=assignment)
            marks_list.append(student_assignment.marks)
        except StudentAssignmentSubmission.DoesNotExist:
            marks_list.append(None)
    
    # Pass data to the template and render it
    context = {
        'assignments': zip(assignments, marks_list),
        'faculty_info': fac_id,
        'course': course,
        'fac_id':fac_id,
    }
    return render(request, 'studmain/stud_assign_list.html', context)


def studfaq(request):
    a=FAQ.objects.all()
    return render(request,'studmain/stud_faq.html',{'faq':a})

def studcontact(request):
    return render(request,'studmain/stud_contact.html')
# def studfeed(request):
#     if request.method == 'POST':
#         feed=feedbackform(request.POST)
#         if feed.is_valid():
#             #handle_upload_file(request.FILES['assignment_file'])
#             model_instance=feed.save(commit=False)
#             model_instance.save()
#             return render(request,'studmain/feedone.html')
#     else:
#         feed=feedbackform()
#     return render(request,'studmain/stud_feed.html',{'form':feed})
# def studpro(request):
#     if request.method == "POST":
#         assignsub=assignsubform(request.POST,request.FILES)
#         if assignsub.is_valid():
#             m=assignsub.save(commit=False)
#             m.save()
#             return render(request,'studmain/assigndone.html')
#     else:
#         assignsub=assignsubform()
#     return render(request,'studmain/studpro.html',{'form':assignsub})
def studassignsub(request):
    if request.method == 'POST':
        fac_id = request.GET.get('fac_id')

        assign=assignsubform(request.POST,request.FILES)
        if assign.is_valid():
            #handle_upload_file(request.FILES['assignment_file'])
            model_instance=assign.save(commit=False)
            model_instance.save()
           
            messages.success(request, 'File uploaded successfully.')
            assignment_data = assign.cleaned_data['assignment_id']

            return redirect(reverse('studassignsub') + f'?assign_id={assignment_data}')
            # return render(request,'facmain/assigndone.html',{'course_id':course_id})
    else:
        course_id = request.GET.get('course_id')
        fac_id = request.GET.get('fac_id')
        assignment_id=request.GET.get('assign_id')
        # fac_ass_ids = FacultyAssignment.objects.filter(fac_id=fac_id, course_id=course_id).values_list('assignment_id', flat=True)
        assignments = Assignment.objects.get(assignment_id=assignment_id)
        student_info = request.session.get('student')
        stud = Student.objects.get(reg_no=student_info['reg_no'])        
        submit_form = assignsubform(initial={'assignment': assignments.assignment_id,'student':stud.reg_no})
        submission = AssignmentSubmission.objects.filter(assignment_id=assignments.assignment_id, reg_no=student_info['reg_no']).order_by('-submission_id').first()
        student_instance = Student.objects.get(reg_no=student_info['reg_no'])
        try:
            student_assignments = StudentAssignmentSubmission.objects.get(reg_no=student_instance, assignment_id=assignments)
            marks = student_assignments.marks
        except StudentAssignmentSubmission.DoesNotExist:
                marks = None

        if submission:
            latest_submission_id = submission.submission_id
        else:
            latest_submission_id = None

        all_submissions = AssignmentSubmission.objects.filter(assignment_id=assignments.assignment_id, reg_no=student_info['reg_no']).order_by('-submission_id').values('submission_id', 'assignment_file_answer')

        all_submission_ids = list(all_submissions)
       
        return render(request, 'studmain/stud_assign_sub.html', {'form': assignments, 'submit_form': submit_form, 'course_id': course_id,'latest_submission_id':latest_submission_id,'all_submission_ids':all_submission_ids,'marks':marks,'fac_id':fac_id})


def submitted(request):
    return HttpResponse('your in the ')
  

def studmodule(request):
    return render(request,'studmain/stud_module.html')

def studgrade(request):
    return render(request,'studmain/stud_grades.html')

def facmain(request):
    faculty = request.session.get('faculty')
    fac_courses = Enrollment.objects.filter(fac_id=faculty['fac_id']).values('course_id').annotate(count=Count('course_id')).order_by()
    courses_info = []
    for fac_course in fac_courses:
        course_details = {}
        course = Course.objects.get(course_id=fac_course['course_id'])
        course_details['course_name'] = course.course_name
        course_details['course_credits'] = course.credits
        course_details['department'] = course.department_name.department_name
        course_details['course_img'] = course.course_img
        course_details['course_id'] = course.course_id
        courses_info.append(course_details)
    print(courses_info)

    return render(request, 'facmain/fac_home.html', {'Course': courses_info})

def facannouncement(request):
    course_id = request.GET.get('course_id', None)
    if request.method == 'POST':
        form = announcementform(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)  # Don't save yet
            fac_id = request.session.get('faculty')
            announcement.save()
            # Save the announcement to the FacultyAnnouncements table for each faculty member
            fac_instance = Faculty.objects.get(fac_id=fac_id['fac_id'])
            try:
                if course_id is not None:
                    course_instance = Course.objects.get(course_id=course_id)
                    FacultyAnnouncements.objects.create(fac_id=fac_instance, notice_id=announcement, course_id=course_instance)
                else:
                    FacultyAnnouncements.objects.create(fac_id=fac_instance, notice_id=announcement)

                return redirect('/facannouncementlist/?course_id={}'.format(course_id))
            except Exception as e:
                print(e)  # Print the exception for debugging
        else:
            print(form.errors)  # Print form validation errors for debugging
    else:
        form = announcementform()  # Create a new form instance

    return render(request, 'facmain/fac_ann.html', {'form': form, 'course_id': course_id})

def facannouncementlist(request):
    course_id = request.GET.get('course_id')
    if course_id:
        announcements = FacultyAnnouncements.objects.filter(course_id=course_id)
        return render(request, 'facmain/fac_ann_list.html', {'announcements': announcements,'course_id':course_id})
    else:
        # Handle the case when no course ID is provided
        return render(request, 'facmain/fac_ann_list.html', {'announcements': None})

def studannouncement(request):
    course_id = request.GET.get('course_id')
    fac_id = request.GET.get('fac_id')
    print(course_id, fac_id)
    if course_id:
        fac_id_inst = Faculty.objects.get(fac_id=fac_id)
        course_id = Course.objects.get(course_id=course_id)
        faculty_announcements = FacultyAnnouncements.objects.filter(course_id=course_id, fac_id=fac_id_inst)
        notice_ids = [fa.notice_id.notice_id for fa in faculty_announcements]  # Access the notice_id directly

        announcements = Announcements.objects.filter(notice_id__in=notice_ids)
        print(announcements)
        return render(request, 'studmain/stud_ann.html', {'announcements': announcements, 'course_id': course_id,'fac_id':fac_id})
    return HttpResponse("No course_id provided")

def facprofile(request):    
    faculty_info = request.session.get('faculty')
    fac = Faculty.objects.get(fac_id=faculty_info['fac_id'])
    fac_dept=FacultyDepartment.objects.get(fac_id=faculty_info['fac_id'])
    fac_mobile = FacultyMobile.objects.filter(fac_id=faculty_info['fac_id']).first()
    faculty = {'fac_id': fac.fac_id,'email':fac.email,'name':fac.first_name,'department':fac_dept.department_name.department_name,'mobile':fac_mobile.mobile_no,'gender':fac.gender}  # Add more fields as needed
    return render(request,'facmain/fac_profile.html',{'details':faculty})

def facDoProfile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        fac_id = request.POST.get('fac_id')
        mobile = request.POST.get('mobile')
        faculty = Faculty.objects.get(fac_id=fac_id)
        try:
            faculty = Faculty.objects.get(fac_id=fac_id)
        except Faculty.DoesNotExist:
            error_message = "Faculty does not exist"
            return HttpResponse(error_message)
        faculty.first_name = name
        faculty.email = email
        if gender=="male":
            faculty.gender = "M"
        else:
            faculty.gender="F"

        faculty.save()
        try:
            faculty_mobile = FacultyMobile.objects.get(fac_id=fac_id)
            faculty_mobile.mobile_no = mobile

            faculty_mobile.save()
        except FacultyMobile.DoesNotExist:

            FacultyMobile.objects.create(fac_id=fac_id, mobile_no=mobile)
        messages.success(request, 'Profile updated successfully.')

        # Redirect to a success page or render the profile page again with updated details
        return redirect('/facprofile/')  # Assuming you have a URL named 'profile' for rendering the profile page
    else:
        # If the request method is not POST, redirect to some error page or handle it accordingly
        error_message = "Invalid request method"
        return HttpResponse(error_message)


def facgocourse(request):
    course_id = request.GET.get('course_id')
    course = Course.objects.get(course_id=course_id)
    faculty_info = request.session.get('faculty')
  # Retrieve all material IDs associated with the current faculty
    fac_mat_ids = FacultyMaterial.objects.filter(fac_id=faculty_info['fac_id']).values_list('material_id', flat=True)
    faculty_materials = Materials.objects.filter(course_id=course_id, material_id__in=fac_mat_ids)

    course_details = {
        'course_name': course.course_name,
        'course_id':course.course_id,
        'materials': faculty_materials,
    }
    print(course_details['materials'])
    return render(request,'facmain/fac_course.html',{'course_details':course_details})

def facDelMat(request):
    material_id=request.GET.get('material_id')
    materials = Materials.objects.get(material_id=material_id)
    materials.delete()
    course_id = request.GET.get('course_id')
    return redirect(f'/facgocourse/?course_id={course_id}')

def facupload(request):
    if request.method == 'POST':
        mat=materialsform(request.POST,request.FILES)

        if mat.is_valid():
            #handle_upload_file(request.FILES['assignment_file'])
            model_instances=mat.save(commit=False)
            model_instances.save()
            faculty_info = request.session.get('faculty')
            fac = Faculty.objects.get(fac_id=faculty_info['fac_id'])
            FacultyMaterial.objects.create(fac_id=fac, material_id=model_instances)
            course = mat.cleaned_data['course_id']
            

            return render(request,'facmain/matdone.html',{'Course':course})
    else:
        mat=materialsform()
    return render(request,'facmain/fac_upload.html',{'form':mat})

def facassigning(request):
    if request.method == 'POST':
        assign=assignmentform(request.POST,request.FILES)
        if assign.is_valid():
            #handle_upload_file(request.FILES['assignment_file'])
            model_instance=assign.save(commit=False)
            model_instance.save()
            faculty_info = request.session.get('faculty')
            course_id=request.GET.get('course_id')
            course = Course.objects.get(course_id=course_id)  # Fetch Course instance
            fac = Faculty.objects.get(fac_id=faculty_info['fac_id'])
            FacultyAssignment.objects.create(fac_id=fac, assignment_id=model_instance,course_id=course)
            return render(request,'facmain/assigndone.html',{'course_id':course_id})
    else:
        course_id=request.GET.get('course_id')
        assign = assignmentform(initial={'course_id': course_id})
    return render(request,'facmain/fac_assign.html',{'form':assign,'course_id':course_id})


def facsub(request):
    # Retrieve relevant data
    faculty_info = request.session.get('faculty')
    course_id = request.GET.get('course_id')
    course = Course.objects.get(course_id=course_id)
    fac_ass_ids = FacultyAssignment.objects.filter(fac_id=faculty_info['fac_id']).values_list('assignment_id', flat=True)
    
    # Filter assignments related to the current course and faculty
    assignments = Assignment.objects.filter(assignment_id__in=fac_ass_ids)
    
    # Pass data to the template and render it
    context = {
        'assignments': assignments,
        'faculty_info': faculty_info,
        'course': course,
    }
    return render(request, 'facmain/fac_assign_list.html', context)

def assignmentstudlist(request):
    faculty_info = request.session.get('faculty')
    course_id = request.GET.get('course_id')
    assignment_id = request.GET.get('assignment_id')
    total_marks = request.GET.get('total_marks')
    
    # Retrieve the list of student registration numbers enrolled in the course
    listofstud = Enrollment.objects.filter(course_id=course_id, fac_id=faculty_info['fac_id']).values_list('reg_no', flat=True)
    
    # Create a list to store tuples of (student_reg_no, marks)
    student_marks = []
    for student_reg_no in listofstud:
        # Check if there's a StudentAssignmentSubmission record for the student and assignment
        try:
            student_instance = Student.objects.get(reg_no=student_reg_no)
            assignment_instance = Assignment.objects.get(assignment_id=assignment_id)
            student_assignment = StudentAssignmentSubmission.objects.get(reg_no=student_instance,assignment_id=assignment_instance)
            marks = student_assignment.marks
        except StudentAssignmentSubmission.DoesNotExist:
            marks = 0
        
        # Append a tuple of (student_reg_no, marks) to the list
        student_marks.append((student_reg_no, marks))
    
    context = {
        'total_marks': total_marks,
        'assignment_id': assignment_id,
        'faculty_info': faculty_info['fac_id'],
        'course_id': course_id,
        'student_marks': student_marks
    }
    
    return render(request, 'facmain/assignmentstudlist.html', context)

def viewassignsub(request):
    faculty_info = request.session.get('faculty')
    course_id = request.GET.get('course_id')
    total_marks = request.GET.get('total_marks')
    assignment_id = request.GET.get('assignment_id')
    stud_id=request.GET.get('student_id')
    # Retrieve the list of student registration numbers enrolled in the course

    # Retrieve assignment submissions for each student along with marks
    submissions = AssignmentSubmission.objects.filter(reg_no=stud_id, assignment_id=assignment_id).order_by('-submission_id').values_list('submission_id', 'assignment_file_answer')
    submission_data = []
    k=0
    for submission_id, assignment_file_answer in submissions:
        # Fetch marks from StudentAssignmentSubmission if available
        marks = StudentAssignmentSubmission.objects.filter(submission_id=submission_id, reg_no=stud_id, assignment_id=assignment_id).values_list('marks', flat=True).first()
        if marks is not None: k=marks
        submission_data.append({
            'submission_id': submission_id,
            'assignment_file_answer': assignment_file_answer,
        })
    print(submission_data)
   
    return render(request, 'facmain/assignsubmitted.html', { 'submission_data': submission_data, 'total_marks': total_marks, 'assignment_id': assignment_id, 'course_id': course_id,'marks':k,'student_id':stud_id})

def submit_marks(request):
    if request.method == 'POST':
        student_reg_no = request.POST.get('student_id')
        submission_id = request.POST.get('submission')
        marks = request.POST.get('marks')
        faculty_info = request.session.get('faculty')
        course_id = request.POST.get('course_id')
        assignment_id = request.POST.get('assignment_id')
        total_marks = request.POST.get('total_marks')
        
        # Validate marks
        
        # Get the Student and Assignment instances
        student_instance = Student.objects.get(reg_no=student_reg_no)
        assignment_instance = Assignment.objects.get(assignment_id=assignment_id)
        submission_instance = AssignmentSubmission.objects.get(pk=submission_id)
    
    
        # Check if StudentAssignmentSubmission record exists for this student and assignment
        try:
            student_assignment = StudentAssignmentSubmission.objects.get(
                reg_no=student_instance,
                assignment_id=assignment_instance
            )
            # Update marks for existing record
            student_assignment.submission_id = submission_instance
            student_assignment.marks = marks
            student_assignment.save()
        except StudentAssignmentSubmission.DoesNotExist:
            # Create a new record if not found
            student_assignment = StudentAssignmentSubmission.objects.create(
                submission_id=submission_instance,
                reg_no=student_instance,
                assignment_id=assignment_instance,
                marks=marks
            )
        messages.success(request, 'Profile updated successfully.')

        # Redirect to viewassignsub with course_id and fac_id in URL
        return redirect(reverse('viewassignsub') + f'?course_id={course_id}&fac_id={faculty_info["fac_id"]}&assignment_id={assignment_id}&total_marks={total_marks}&student_id={student_reg_no}&marks={marks}')

    # Return method not allowed for other HTTP methods
    return HttpResponse("Method not allowed", status=405)
def testdone(request):
    return render(request,'facmain/fac_course.html')

def assigndone(request):
    return render(request,'facmain/assigndone.html')

def matdone(request):
    return render(request,'facmain/matdonedone.html')



def facassign(request):
    return render(request,'facmain/fac_assign.html')

def facfaq(request):
    a=FAQ.objects.all()
    return render(request,'facmain/fac_faq.html',{'faq':a})
    
def faccontact(request):
    return render(request,'facmain/fac_contact.html')


def posting(request):
    value=request.POST

    subject='quiz link'
    message='please use this below link for test.LINK:"https://forms.office.com/Pages/ResponsePage.aspx?id=o835AF4H5USqC6ujrdZTn1ZzWpbksglCn4c6JT8KiTZURERMQUoxMjJCTzZKMkxKTk9MS1FUSTNSMy4u" ALL THE BEST!  Thank You!'
    from_email=settings.EMAIL_HOST_USER
    to_list=[settings.EMAIL_HOST_USER]
    send_mail(subject,message,from_email,to_list,fail_silently=True)
    return render(request,'facmain/testdone.html')
    