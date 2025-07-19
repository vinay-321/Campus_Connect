from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):

    ROLE_CHOICES=(
        ('admin','Admin'),
        ('faculty','Faculty'),
        ('student', 'Student')
    )

    role=models.CharField(max_length=15,choices=ROLE_CHOICES)
    



class Department(models.Model):
    department_name=models.CharField(max_length=50)


class SubjectsList(models.Model):
    department=models.ForeignKey(Department,on_delete=models.CASCADE,related_name='subjects_list')
    subject_name=models.CharField(max_length=100)
    subject_code=models.CharField(max_length=50)
    
class Semester(models.Model):
    semester=models.CharField(max_length=10)
    subject=models.ForeignKey(SubjectsList,on_delete=models.CASCADE,related_name='subjects')







class StudentProfile(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,limit_choices_to={'role':'student'})
    enrollment_no=models.IntegerField(unique=True)
    department= models.ForeignKey(Department,on_delete=models.CASCADE) 
    batch = models.CharField(max_length=20) 
    mobile =models.BigIntegerField() 





class Faculty(models.Model):
   faculty=models.ForeignKey(CustomUser,on_delete=models.CASCADE,limit_choices_to={'role':'faculty'})
   employee_id=models.CharField(max_length=20,unique=True)
   Department=models.ForeignKey(Department,on_delete=models.CASCADE,related_name='fac_department')
   desgination=models.CharField(max_length=20)



class Assignment(models.Model):
    title=models.CharField(max_length=50)
    description=models.CharField(max_length=50)
    assignment_file=models.FileField(upload_to='assginment/')
    subject=models.ForeignKey(SubjectsList,on_delete=models.CASCADE)
    created_by=models.ForeignKey(Faculty,on_delete=models.CASCADE)
    due_date=models.DateField()



class AssignmentSubmission(models.Model):
    
    STATUS=(
        ('submitted','Submitted'),
        ('reviewed','Reviewed'),
        ('rejected','Rejected'),

      )

    assignment=models.ForeignKey(Assignment,on_delete=models.CASCADE)
    student=models.ForeignKey(StudentProfile,on_delete=models.CASCADE)
    submitted_assignment=models.FileField(upload_to='submitted_assginment/')
    status=models.CharField(max_length=20,choices=STATUS)
    feedback=models.CharField(max_length=100 ,null=True,blank=True)


class Attendance(models.Model):

     STATUS=(
         ('present','present'),
         ('absent','absent')
     )
     student=models.ForeignKey(StudentProfile,on_delete=models.CASCADE)
     date=models.DateField(auto_now_add=True)
     subject=models.ForeignKey(SubjectsList,on_delete=models.CASCADE)
     status=models.CharField(max_length=20,choices=STATUS)


















