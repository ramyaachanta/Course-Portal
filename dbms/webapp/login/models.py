from django.db import models

from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import login,logout
# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    name= models.CharField(max_length=100)
    email= models.CharField(max_length=100)
    Type = models.CharField(max_length = 50) 
    def _str_(self):
        return self.username


class Student(models.Model):
    reg_no=models.CharField(max_length=100,primary_key = True)
    stud_pwd=models.CharField(max_length=100)
    stud_name=models.CharField(max_length=100)
    stud_email=models.CharField(max_length=100)
    #dept=models.CharField(max_length=100)
    stud_mobile=models.IntegerField() 
    sem_No=models.CharField(max_length=100)
    # ​stud_gender=models.CharField(max_length=100)
    year=models.IntegerField()
    cgpa=models.FloatField()
    def _str_(self):
        return self.reg_no


class Faculty(models.Model):
    fac_id=models.CharField(max_length=100,primary_key = True)
    fac_pwd=models.CharField(max_length=100)
    fac_name=models.CharField(max_length=100)
    fac_email=models.CharField(max_length=100)
    fac_mobile=models.IntegerField()
    dept_name=models.CharField(max_length=100)
    # ​fac_gender=models.CharField(max_length=100)
    def _str_(self):
        return self.fac_id
    


class Announcements(models.Model):
    notice_id=models.CharField(max_length=100,primary_key = True)
    title=models.CharField(max_length=100)
    description=models.CharField(max_length=100)
    publish_date=models.DateField(auto_now_add=True)
    
    def _str_(self):
        return self.notice_id

class Course(models.Model):
    course_id=models.CharField(max_length=100,primary_key = True)
    course_name=models.CharField(max_length=100)
    course_credits=models.CharField(max_length=100)
    course_type=models.CharField(max_length=100)
    course_status=models.CharField(max_length=100)
    course_img=models.ImageField( default="")

class Department(models.Model):
    dept_name=models.CharField(max_length=100,primary_key = True)
    no_of_sec=models.CharField(max_length=100)
    def _str_(self):
        return self.dept_name


class assignsub(models.Model):
    
    assignment_ans=models.FileField("ENTER FILE")

class assignment(models.Model):
    assignment_file=models.FileField("ENTER FILE:")
    marks=models.IntegerField("ENTER MARKS:")
    message=models.CharField("ENTER MESSAGE:",max_length=100)
   

class materials(models.Model):
    lec_title=models.CharField("ENTER TITLE:",max_length=100,primary_key = True)
    lec_pdf= models.FileField("ENTER DOCUMENT:",max_length=100)
    def _str_(self):
        return self.lec_title

class faq(models.Model):
    faq_id=models.CharField(max_length=100,primary_key = True)
    faq_qsn=models.CharField(max_length=100)
    faq_asn=models.CharField(max_length=100)
    def _str_(self):
        return self.faq_id

class feedback(models.Model):
    feed_id=models.AutoField(max_length=100,primary_key = True)
    reg_no=models.CharField("enter your rollno:",max_length=100)
    descp=models.CharField("message:",max_length=100)
    def _str_(self):
        return self.feed_id


