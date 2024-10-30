
from django.db import models
from django.db.models import UniqueConstraint

# Custom Domain-like Fields

class FileField(models.FileField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_length = 100

class CreditHoursField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_digits = 5
        self.decimal_places = 0

class QuestionField(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_length = 50

class OptionsField(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_length = 50

class AnswerField(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_length = 50

class UserTypeField(models.CharField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_length = 50

# Models

class Department(models.Model):
    department_name = models.CharField(primary_key=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'department'
    
    def __str__(self):
        return self.department_name


class Faculty(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    
    fac_id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=20, blank=True, null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    joining_date = models.DateField()
   
    class Meta:
        managed = False
        db_table = 'faculty'

    def __str__(self):
        return f"{self.fac_id} - {self.first_name} {self.last_name}"

class FacultyMobile(models.Model):
    mobile_no = models.CharField(primary_key=True,max_length=20)
    fac = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    
    class Meta:
        managed = False
        db_table = 'facultymobile'

    def __str__(self):
        return str(self.mobile_no)

class Course(models.Model):
    COURSE_TYPE_CHOICES = [
        ('F2F', 'Face to Face'),
        ('<50%-O', '<50% Online'),
        ('100%-O', '100% Online')
    ]
    course_id = models.IntegerField(primary_key=True)
    course_name = models.CharField(max_length=100)
    credits = CreditHoursField()
    department_name = models.ForeignKey(Department,  models.DO_NOTHING, db_column='department_name',blank=True, null=True)
    course_type=models.CharField(max_length=20, choices=COURSE_TYPE_CHOICES)
    course_img=models.ImageField( default="")

    class Meta:
        managed = False
        db_table = 'course'

    def __str__(self):
        return str(self.course_id)




class FacultyDepartment(models.Model):
    fac_id = models.ForeignKey(Faculty, on_delete=models.CASCADE, db_column='fac_id', primary_key=True)
    department_name = models.ForeignKey(Department, on_delete=models.CASCADE, db_column='department_name')

    class Meta:
        managed = False
        db_table = 'facultydepartment'
        unique_together = (('fac_id', 'department_name'),)

    def __str__(self):
        return f"{self.fac_id} - {self.department_name}"



class Student(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    password = models.CharField(max_length=20, blank=True, null=True)
    reg_no = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    dob = models.DateField()
    cgpa = models.FloatField()
    year = models.IntegerField()
    sem_no = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    
    class Meta:
        managed = False
        db_table = 'student'

    def __str__(self):
        return f"{self.reg_no} - {self.first_name} {self.last_name}"
    
class StudentDepartment(models.Model):
    reg_no = models.ForeignKey(Student, on_delete=models.CASCADE,db_column='reg_no',primary_key=True)
    department_name = models.ForeignKey(Department, on_delete=models.CASCADE,db_column='department_name')

    class Meta:
        managed = False
        db_table = 'studentdepartment'
        unique_together = (('reg_no', 'department_name'),)

    def __str__(self):
        return f"{self.reg_no} - {self.department_name}"


class StudentMobile(models.Model):
    mobile_no = models.CharField(primary_key=True,max_length=20)
    reg_no = models.ForeignKey(Student, on_delete=models.CASCADE,db_column='reg_no')

    class Meta:
        managed = False
        db_table = 'studentmobile'

    def __str__(self):
        return f"{self.reg_no} - {self.mobile_no}"

class Feedback(models.Model):
    feedback_id = models.AutoField(max_length=50, primary_key=True)
    fac_id = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    reg_no = models.IntegerField()
    feedback_ans = models.CharField(max_length=500)
    feedback_question = models.CharField(max_length=50)
    date_submitted = models.DateField()
    course_id = models.ForeignKey(Course, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'feedback'

    def __str__(self):
        return self.feedback_id

class Assignment(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    title=models.CharField(default="",max_length=100)
    total_marks = models.FloatField()
    message = models.CharField(max_length=500)
    assignment_file_question = FileField()
    end_time = models.DateTimeField()
    start_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'assignment'

    def __str__(self):
        return str(self.assignment_id)


class AssignmentSubmission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    message = models.CharField(max_length=500)
    assignment_file_answer = models.FileField(upload_to='assignment_submissions/')
    reg_no = models.ForeignKey(Student, on_delete=models.CASCADE,db_column='reg_no')
    assignment_id = models.ForeignKey(Assignment, on_delete=models.CASCADE,db_column='assignment_id')
    
    class Meta:
        db_table = 'assignmentsubmission'

    def __str__(self):
        return f"{self.reg_no} - {self.assignment_id} - Submission {self.submission_id}"


class FacultyAssignment(models.Model):
    assignment_id = models.ForeignKey(Assignment, on_delete=models.CASCADE,db_column='assignment_id')
    fac_id = models.ForeignKey(Faculty, on_delete=models.CASCADE,db_column='fac_id')
    course_id=models.ForeignKey(Course, on_delete=models.CASCADE,db_column='course_id')
    
    class Meta:
        managed = False
        db_table = 'facultyassignment'
        unique_together = (('assignment_id', 'fac_id', 'course_id'),)

    
    def __str__(self):
        return f"{self.fac_id} - {self.assignment_id} - {self.course_id}"

class StudentAssignmentSubmission(models.Model):
    submission_id = models.ForeignKey(AssignmentSubmission, on_delete=models.CASCADE,db_column='submission_id')
    reg_no = models.ForeignKey(Student, on_delete=models.CASCADE,db_column='reg_no')
    assignment_id = models.ForeignKey(Assignment, on_delete=models.CASCADE,db_column='assignment_id')  # Foreign key to Assignment model
    marks = models.FloatField()  # Field to store the marks

    class Meta:
        managed = False
        db_table = 'studentassignmentsubmission'
        unique_together = (('submission_id', 'reg_no', 'assignment_id'),)

    def __str__(self):
        return f"{self.reg_no} - {self.assignment_id} - Submission {self.submission_id}"



class Enrollment(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE,db_column='course_id')
    fac_id = models.ForeignKey(Faculty, on_delete=models.CASCADE,db_column='fac_id')
    reg_no = models.ForeignKey(Student,on_delete=models.CASCADE,db_column='reg_no')
    enrolled_on = models.DateField()


    class Meta:
        managed = False
        db_table = 'enrollment'
        unique_together = (('course_id', 'fac_id', 'reg_no'),)

    def __str__(self):
        return f"{self.course_id} - {self.reg_no}"

class Materials(models.Model):
    material_id = models.AutoField(primary_key=True)
    material_file = FileField()
    material_title=models.CharField(max_length=100)
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE,db_column='course_id')
    description=models.CharField(max_length=200,default='')
   
    class Meta:
        managed = False
        db_table = 'materials'

    def __str__(self):
        return str(self.material_id)

class FacultyMaterial(models.Model):
    fac_id = models.ForeignKey(Faculty, on_delete=models.CASCADE,db_column='fac_id')
    material_id = models.ForeignKey(Materials, on_delete=models.CASCADE,db_column='material_id', primary_key=True)
    
    class Meta:
        managed = False
        db_table = 'facultymaterial'
        unique_together = (('fac_id', 'material_id'),)


    def __str__(self):
        return f"{self.fac_id} - {self.material_id}"


class FAQ(models.Model):
    faq_id = models.AutoField(primary_key=True)
    faq_qsn = QuestionField()
    faq_ans = AnswerField()
    
    class Meta:
        managed = False
        db_table = 'faq'

    def __str__(self):
        return str(self.faq_id)

class Announcements(models.Model):
    publish_date = models.DateTimeField()
    notice_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=500)
    title = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'announcements'

    def __str__(self):
        return self.title

class FacultyAnnouncements(models.Model):
    fac_id = models.ForeignKey(Faculty, on_delete=models.CASCADE,db_column='fac_id')
    notice_id = models.ForeignKey(Announcements,on_delete=models.CASCADE,db_column='notice_id')
    course_id=models.ForeignKey(Course,on_delete=models.CASCADE,db_column='course_id')

    class Meta:
        managed = False
        db_table = 'facultyannouncements'
        unique_together = (('fac_id','course_id'),)


    def __str__(self):
        return f"{self.fac_id} - {self.notice_id}"

 

class StudentAnnouncements(models.Model):
    reg_no = models.ForeignKey(Student, on_delete=models.CASCADE)
    notice_id = models.ForeignKey(Announcements,on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'studentannouncements'
        unique_together = (('reg_no', 'notice_id'),)


    def __str__(self):
        return f"{self.reg_no} - {self.notice_id}"


# class FacultyFAQ(models.Model):
#     fac = models.ForeignKey(Faculty, on_delete=models.CASCADE)
#     faq_id = models.IntegerField(primary_key=True)

#     def __str__(self):
#         return f"{self.fac} - {self.faq_id}"
# class StudentFAQ(models.Model):
#     reg_no = models.ForeignKey(Student, on_delete=models.CASCADE)
#     faq_id = models.IntegerField(primary_key=True)

#     def __str__(self):
#         return f"{self.reg_no} - {self.faq_id}"