from rest_framework import serializers

from .models import *

class SignupSerializer(serializers.ModelSerializer):

    class Meta:
        model=CustomUser
        fields= ['id','username','password','first_name','last_name','email','role','is_staff']



class DepartmentSerliazer(serializers.ModelSerializer):
    class Meta:
        model=Department
        fields='__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model=SubjectsList
        fields='__all__'

class SemesterSerializer(serializers.ModelSerializer):
    subject_name=serializers.ReadOnlyField(source='subject.subject_name')
    # code=serializers.ReadOnlyField(source='subject.subject_code')
    
    class Meta:
        model=Semester
        fields='__all__'



class StudentProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    email = serializers.ReadOnlyField(source='user.email')
    class Meta:
        model=StudentProfile
        fields='__all__'



class FacultySerializer(serializers.ModelSerializer):
    first_name=serializers.ReadOnlyField(source='faculty.first_name')
    last_name=serializers.ReadOnlyField(source='faculty.last_name')
    email=serializers.ReadOnlyField(source='faculty.email')
    department_name=serializers.ReadOnlyField(source='Department.department_name')
    


    class Meta:
        model=Faculty
        fields='__all__'



class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Assignment
        fields='__all__'



class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model=AssignmentSubmission
        fields='__all__'

class AttendanceSerializer(serializers.ModelSerializer):

    first_name= serializers.ReadOnlyField(source='student.user.first_name')
    last_name= serializers.ReadOnlyField(source='student.user.last_name')
    class Meta:
        model=Attendance
        fields='__all__'




class ResourcesSerializer(serializers.ModelSerializer):
    class Meta:
        model=Resources
        fields='__all__'










