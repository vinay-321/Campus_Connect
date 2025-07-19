from django.shortcuts import render
from .models import *
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from datetime import date
from  rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.permissions import IsAdminUser,IsAuthenticated,IsAuthenticatedOrReadOnly,AllowAny
from rest_framework.authentication import TokenAuthentication



# Create your views here.
class SignupView(APIView):
   authentication_classes=[TokenAuthentication]
   permission_classes=[IsAuthenticated]
   def get(self,request):
        user=CustomUser.objects.all()
        serializer_data=SignupSerializer(user,many=True)
        return Response({'message':'user list','data':serializer_data.data},status=status.HTTP_200_OK)
    

   def post(self,request):
      data=request.data.copy()
      if data.get('role').lower()=='admin':
         data['is_staff']=True
      serializer_data=SignupSerializer(data=data)
      if serializer_data.is_valid():
         user=serializer_data.save()
         user.set_password(request.data.get('password')) 
         user.save()
         return Response({'message':'User Created Successfull'},status=status.HTTP_201_CREATED)
      return Response(serializer_data.errors,status=status.HTTP_400_BAD_REQUEST)
    
   def patch(self,request):
      # print(request.user.role)
      # if request.user.role !='admin':
      #    return Response({'message':'you have not  permision to perform this action'},status=status.HTTP_400_BAD_REQUEST)
      data=request.data
      user_id=data.get('user_id')
      if not CustomUser.objects.filter(id=user_id).exists():
         return Response({'message':f"'subject doesn't exists'"},status=status.HTTP_400_BAD_REQUEST)
      user=CustomUser.objects.get(id=user_id)
      serializer_data= SignupSerializer(user,data=data,partial=True)
      if serializer_data.is_valid():
         user=serializer_data.save()
         user.set_password(request.data.get('password')) 
         user.save()
         return Response({'message':'User Updated Successfully','data':serializer_data.data},status=status.HTTP_200_OK)
      return Response({'message':serializer_data.errors},status=status.HTTP_400_BAD_REQUEST)
   

   def delete(self,request):
      if request.user.role !='admin':
         return Response({'message':'you have not  permision to perform this action'},status=status.HTTP_400_BAD_REQUEST)
      user_id=request.data.get('user_id')
      if not CustomUser.objects.filter(id=user_id).exists():
         return Response({'message':f"user dosen't exists"},status=status.HTTP_400_BAD_REQUEST)
      CustomUser.objects.get(id=user_id).delete()
      return Response({'message':'User delete successfully'},status=status.HTTP_200_OK)
    
    

    



class LoginView(APIView):
   def post(self,request):
      data=request.data
      username=data.get('username')
      password=data.get('password')
      user=authenticate(username=username,password=password)
      token,object=Token.objects.get_or_create(user=user)
      if user:
         return Response({'message':'login sccessfully','token':token.key},status=status.HTTP_200_OK)
      else:
         return Response({'message':'Invalid Credentials'},status=status.HTTP_400_BAD_REQUEST)
      



class StudentProfileView(APIView):
   authentication_classes=[TokenAuthentication]
   permission_classes=[IsAuthenticated]
   def get(self,request):
      students=StudentProfile.objects.all()
      serializer_data=StudentProfileSerializer(students,many=True)
      return Response({'message':'Student List','data':serializer_data.data},status=status.HTTP_200_OK)
   
   def post(self,request):
      if request.user.role not in ['admin', 'faculty']:
         return Response({'message':'you have not  permision to perform this action'},status=status.HTTP_400_BAD_REQUEST)
      data=request.data
      serializer_data=StudentProfileSerializer(data=data)
      if serializer_data.is_valid():
         serializer_data.save()
         return Response({'message':'Student Profile Created Successfully'},status=status.HTTP_201_CREATED)
      return Response({'message':serializer_data.errors},status=status.HTTP_400_BAD_REQUEST)

   def patch(self,request):
      if request.user.role not in ['admin', 'faculty']:
         return Response({'message':'you have not  permision to perform this action'},status=status.HTTP_400_BAD_REQUEST)
      data=request.data
      student_id=data.get('student_id')
      if not StudentProfile.objects.filter(id=student_id).exists():
         return Response({'message':f"'student doesn't exists'"},status=status.HTTP_400_BAD_REQUEST)
      student=StudentProfile.objects.get(id=student_id)
      serializer_data= StudentProfileSerializer(student,data=data,partial=True)
      if serializer_data.is_valid():
         serializer_data.save()
         return Response({'message':'data Updated Successfully','data':serializer_data.data},status=status.HTTP_200_OK)
      return Response({'message':serializer_data.errors},status=status.HTTP_400_BAD_REQUEST)
   

   def delete(self,request):
      if request.user.role not in ['admin', 'faculty']:
         return Response({'message':'you have not  permision to perform this action'},status=status.HTTP_400_BAD_REQUEST)
      student_id=request.data.get('student_id')
      if not StudentProfile.objects.filter(id=student_id).exists():
         return Response({'message':f"student dosen't exists"},status=status.HTTP_400_BAD_REQUEST)
      StudentProfile.objects.get(id=student_id).delete()
      return Response({'message':'student delete successfully'},status=status.HTTP_200_OK)
   

class DepartmentView(APIView):
   authentication_classes=[TokenAuthentication]
   permission_classes=[IsAuthenticated]
   def get(self,request):
      departments=Department.objects.all()
      serializer_data=DepartmentSerliazer(departments,many=True)
      return Response({'message':'Departments List','data':serializer_data.data},status=status.HTTP_200_OK)
   
   def post(self,request):
      if request.user.role!='admin':
         return Response({'message':'you have not  permision to perform this action'},status=status.HTTP_400_BAD_REQUEST)
      data=request.data
      department_name= data.get('department_name')
      if  Department.objects.filter(department_name=department_name).exists():
          return Response({'message':'already  department exist '},status=status.HTTP_400_BAD_REQUEST)
      serializer_data=DepartmentSerliazer(data=data)
      if serializer_data.is_valid():
         serializer_data.save()
         return Response({'message':'Department Add Successfully'},status=status.HTTP_201_CREATED)
      return Response({'message':serializer_data.errors},status=status.HTTP_400_BAD_REQUEST)


   def patch(self,request):
      data=request.data
      department_id=data.get('department_id')
      if request.user.role !='admin':
         return Response({'message':'you have not  permision to perform this action'},status=status.HTTP_400_BAD_REQUEST)
      if not Department.objects.filter(id=department_id).exists():
         return Response({'message':f"'department doesn't exists'"},status=status.HTTP_400_BAD_REQUEST)
      student=Department.objects.get(id=department_id)
      serializer_data= DepartmentSerliazer(student,data=data,partial=True)
      if serializer_data.is_valid():
         serializer_data.save()
         return Response({'message':'department Updated Successfully','data':serializer_data.data},status=status.HTTP_200_OK)
      return Response({'message':serializer_data.errors},status=status.HTTP_400_BAD_REQUEST)
   

   def delete(self,request):
      department_id=request.data.get('department_id')
      if request.user.role !='admin':
         return Response({'message':'you have not  permision to perform this action'},status=status.HTTP_400_BAD_REQUEST)
      if not Department.objects.filter(id=department_id).exists():
         return Response({'message':f"de dosen't exists"},status=status.HTTP_400_BAD_REQUEST)
      Department.objects.get(id=department_id).delete()
      return Response({'message':'Department delete successfully'},status=status.HTTP_200_OK)
   



class SubjectsView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request):
      subjects=SubjectsList.objects.all()
      serializer_data=SubjectSerializer(subjects,many=True)
      return Response({'message':'Subjects List','data':serializer_data.data},status=status.HTTP_200_OK)
   
    def post(self,request):
      if request.user.role !='admin':
         return Response({'message':'you have not  permision to perform this action'},status=status.HTTP_400_BAD_REQUEST)
      data=request.data
      serializer_data=SubjectSerializer(data=data)
      if serializer_data.is_valid():
         serializer_data.save()
         return Response({'message':'Subject  Created Successfully'},status=status.HTTP_201_CREATED)
      return Response({'message':serializer_data.errors},status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request):
      if request.user.role !='admin':
         return Response({'message':'you have not  permision to perform this action'},status=status.HTTP_400_BAD_REQUEST)
      data=request.data
      subject_id=data.get('subject_id')
      if not SubjectsList.objects.filter(id=subject_id).exists():
         return Response({'message':f"'subject doesn't exists'"},status=status.HTTP_400_BAD_REQUEST)
      subject=SubjectsList.objects.get(id=subject_id)
      serializer_data= SubjectSerializer(subject,data=data,partial=True)
      if serializer_data.is_valid():
         serializer_data.save()
         return Response({'message':'data Updated Successfully','data':serializer_data.data},status=status.HTTP_200_OK)
      return Response({'message':serializer_data.errors},status=status.HTTP_400_BAD_REQUEST)
   

    def delete(self,request):
      if request.user.role !='admin':
         return Response({'message':'you have not  permision to perform this action'},status=status.HTTP_400_BAD_REQUEST)
      subject_id=request.data.get('subject_id')
      if not StudentProfile.objects.filter(id=subject_id).exists():
         return Response({'message':f"subject dosen't exists"},status=status.HTTP_400_BAD_REQUEST)
      StudentProfile.objects.get(id=subject_id).delete()
      return Response({'message':'subject delete successfully'},status=status.HTTP_200_OK)
    



    

class SemesterView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request):
      semester =Semester.objects.all()
      serializer_data=SemesterSerializer(semester,many=True)
      return Response({'message':'Semester List','data':serializer_data.data},status=status.HTTP_200_OK)
   
    def post(self,request):
      # if request.user.role !='admin':
      #    return Response({'message':'you have not  permision to perform this action'},status=status.HTTP_400_BAD_REQUEST)
      data=request.data
      serializer_data=SemesterSerializer(data=data)
      
      if serializer_data.is_valid():
         serializer_data.save()
         return Response({'message':'Semester  Created Successfully'},status=status.HTTP_201_CREATED)
      return Response({'message':serializer_data.errors},status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request):
      if request.user.role !='admin':
         return Response({'message':'you have not  permision to perform this action'},status=status.HTTP_400_BAD_REQUEST)
      data=request.data
      semester_id=data.get('semester_id')
      if not Semester.objects.filter(id=semester_id).exists():
         return Response({'message':f"'Semester doesn't exists'"},status=status.HTTP_400_BAD_REQUEST)
      semester=Semester.objects.get(id=semester_id)
      serializer_data= SemesterSerializer(semester,data=data,partial=True)
      if serializer_data.is_valid():
         serializer_data.save()
         return Response({'message':'data Updated Successfully','data':serializer_data.data},status=status.HTTP_200_OK)
      return Response({'message':serializer_data.errors},status=status.HTTP_400_BAD_REQUEST)
   

    def delete(self,request):
      if request.user.role !='admin':
         return Response({'message':'you have not  permision to perform this action'},status=status.HTTP_400_BAD_REQUEST)
      semester_id=request.data.get('semester_id')
      if not Semester.objects.filter(id=semester_id).exists():
         return Response({'message':f"semester dosen't exists"},status=status.HTTP_400_BAD_REQUEST)
      Semester.objects.get(id=semester_id).delete()
      return Response({'message':'semester delete successfully'},status=status.HTTP_200_OK)
    


class FacultyView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request):
      if request.user.role !='admin':
         return Response({'message':'you have not  permision to perform this action'},status=status.HTTP_400_BAD_REQUEST)
      semester =Faculty.objects.all()
      serializer_data=FacultySerializer(semester,many=True)
      return Response({'message':'Faculty List','data':serializer_data.data},status=status.HTTP_200_OK)
   
    def post(self,request):
      if request.user.role !='admin':
         return Response({'message':'you have not  permision to perform this action'},status=status.HTTP_400_BAD_REQUEST)
      data=request.data
      serializer_data=FacultySerializer(data=data)
      if serializer_data.is_valid():
         serializer_data.save()
         return Response({'message':'Faculty  Created Successfully'},status=status.HTTP_201_CREATED)
      return Response({'message':serializer_data.errors},status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request):
      if request.user.role !='admin':
         return Response({'message':'you have not  permision to perform this action'},status=status.HTTP_400_BAD_REQUEST)
      data=request.data
      faculty_id=data.get('faculty_id')
      if not Faculty.objects.filter(id=faculty_id).exists():
         return Response({'message':f"'faculty doesn't exists'"},status=status.HTTP_400_BAD_REQUEST)
      faculty=Faculty.objects.get(id=faculty_id)
      serializer_data= FacultySerializer(faculty,data=data,partial=True)
      if serializer_data.is_valid():
         serializer_data.save()
         return Response({'message':'data Updated Successfully','data':serializer_data.data},status=status.HTTP_200_OK)
      return Response({'message':serializer_data.errors},status=status.HTTP_400_BAD_REQUEST)
   

    def delete(self,request):
      if request.user.role !='admin':
         return Response({'message':'you have not  permision to perform this action'},status=status.HTTP_400_BAD_REQUEST)
      faculty_id=request.data.get('faculty_id')
      if not Semester.objects.filter(id=faculty_id).exists():
         return Response({'message':f"semester dosen't exists"},status=status.HTTP_400_BAD_REQUEST)
      Semester.objects.get(id=faculty_id).delete()
      return Response({'message':'semester delete successfully'},status=status.HTTP_200_OK)
    


class AssignmentView(APIView):
     authentication_classes=[TokenAuthentication]
     permission_classes=[IsAuthenticated]
    
     def get(self,request):
      assignment =Assignment.objects.all()
      serializer_data=AssignmentSerializer(assignment,many=True)
      return Response({'message':'Assignment List','data':serializer_data.data},status=status.HTTP_200_OK)
   
     def post(self,request):
      if request.user.role !='faculty':
         return Response({'message':'you have not  permision to perform this action','response_code':400})
      data=request.data
      status=request.data('status')

      
      serializer_data=AssignmentSerializer(data=data)
      if serializer_data.is_valid():
         serializer_data.save()
         return Response({'message':'Assignment  Created Successfully','response_code':200})
      return Response({'message':serializer_data.errors,'response_code':400})
     

     def patch(self,request):
        if request.user.role !='faculty':
         return Response({'message':'you have not  permision to perform this action'},status=status.HTTP_400_BAD_REQUEST)
        data=request.data
        assignment_id=data.get('assignment_id')
        if not Assignment.objects.filter(id=assignment_id).exists():
           return Response({'message':f"'assignment id  doesn't exists'"},status=status.HTTP_400_BAD_REQUEST)
        assignment=Assignment.objects.get(id=assignment_id)
        serializers_data=AssignmentSerializer(assignment,data=data,partial=True)
        if serializers_data.is_valid():
           serializers_data.save()
           return Response({'message':'data Updated Successfully','data':serializers_data.data},status=status.HTTP_200_OK)
        return Response({'message':'data updated Successfully'},status=status.HTTP_400_BAD_REQUEST )
         

   

     def delete(self,request):
      if request.user.role !='faculty':
         return Response({'message':'you have not  permision to perform this action'},status=status.HTTP_400_BAD_REQUEST)
      assignment_id=request.data.get('assignment_id')
      if not Assignment.objects.filter(id=assignment_id).exists():
         return Response({'message':f"assignment dosen't exists"},status=status.HTTP_400_BAD_REQUEST)
      Assignment.objects.get(id=assignment_id).delete()
      return Response({'message':'assignment delete successfully'},status=status.HTTP_200_OK)
     


     
class AssignmentSubmissionView(APIView):
     authentication_classes=[TokenAuthentication]
     permission_classes=[IsAuthenticated]
     def get(self,request):
      assignment =AssignmentSubmission.objects.all()
      serializer_data=AssignmentSubmissionSerializer(assignment,many=True)
      return Response({'message':'Assignment Submitted List','data':serializer_data.data},status=status.HTTP_200_OK)
   
     def post(self,request):
      if request.user.role !='student':
         return Response({'message':'you have not  permision to perform this action'},status=status.HTTP_400_BAD_REQUEST)
      data=request.data
      status_id= data.get('status')
      if AssignmentSubmission.objects.filter(status=status_id).exists():
         return Response({'message':f"'you already Uploaded assignment'",'response_code':400})
      serializer_data=AssignmentSubmissionSerializer(data=data)
      if serializer_data.is_valid():
         serializer_data.save()
         return Response({'message':'Assignment Submitted Successfully'},status=status.HTTP_201_CREATED)
      return Response({'message':serializer_data.errors},status=status.HTTP_400_BAD_REQUEST)

     def patch(self,request):
      if request.user.role !='faculty':
         return Response({'message':'you have not  permision to perform this action'},status=status.HTTP_400_BAD_REQUEST)
      data=request.data
      submission_id=data.get('submission_id')
      if not AssignmentSubmission.objects.filter(id= submission_id).exists():
         return Response({'message':f"'assignment doesn't exists'"},status=status.HTTP_400_BAD_REQUEST)
      submission=AssignmentSubmission.objects.get(id= submission_id)
      serializer_data= AssignmentSubmissionSerializer( submission,data=data,partial=True)
      if serializer_data.is_valid():
         serializer_data.save()
         return Response({'message':'data Updated Successfully','data':serializer_data.data},status=status.HTTP_200_OK)
      return Response({'message':serializer_data.errors},status=status.HTTP_400_BAD_REQUEST)
   

     def delete(self,request):
      if request.user.role !='faculty':
         return Response({'message':'you have not  permision to perform this action'},status=status.HTTP_400_BAD_REQUEST)
      submission_id=request.data.get('submission_id')
      if not AssignmentSubmission.objects.filter(id=submission_id).exists():
         return Response({'message':f"submission id dosen't exists"},status=status.HTTP_400_BAD_REQUEST)
      AssignmentSubmission.objects.get(id=submission_id).delete()
      return Response({'message':'submission  deleted successfully'},status=status.HTTP_200_OK)
     


class AttendanceView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self,request):
      assignment =Attendance.objects.all()
      serializer_data=AttendanceSerializer(assignment,many=True)
      return Response({'message':'Attendance  List','data':serializer_data.data},status=status.HTTP_200_OK)

    def post(self,request):
      if request.user.role !='faculty':
         return Response({'message':'you have not  permision to perform this action'},status=status.HTTP_400_BAD_REQUEST)
      data=request.data
      today=date.today()
      student=data.get('student')
      if not StudentProfile.objects.filter(id=student).exists():
         return Response({'message':'student does not exist'},status=status.HTTP_400_BAD_REQUEST)
      if student:
         if Attendance.objects.filter(student=student,date=today).exists():
             return Response({'message':'you have alreday Marked attendance'},status=status.HTTP_400_BAD_REQUEST)

      serializer_data=AttendanceSerializer(data=data)
      if serializer_data.is_valid():
         serializer_data.save()
         return Response({'message':'Attendance of Students'},status=status.HTTP_200_OK)
      return Response({'message':serializer_data.errors},status=status.HTTP_400_BAD_REQUEST)
    


class StudentAttendanceView(APIView):
   authentication_classes=[TokenAuthentication]
   permission_classes=[IsAuthenticatedOrReadOnly]
   def get(self,request):
      attendance=Attendance.objects.all()
      serializer_data=AttendanceSerializer(attendance,many=True)
      return Response({'message':'Attendance list of Student','data':serializer_data.data},status=status.HTTP_200_OK)
   

class SubmissionListView(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticatedOrReadOnly]
    def get(self,request):
      submission_list=AssignmentSubmission.objects.all()
      serializer_data=AssignmentSubmissionSerializer(submission_list,many=True)
      return Response({'message':' list of Assignment Submission','data':serializer_data.data},status=status.HTTP_200_OK)
   
   # class StudentAttendanceView(APIView):
   #  authentication_classes=[TokenAuthentication]
   #  permission_classes=[IsAuthenticatedOrReadOnly]
   #  def get(self,request):
   #    attendance=Attendance.objects.all()
   #    serializer_data=AttendanceSerializer(attendance,many=True)
   #    return Response({'message':'Attendance list of Student','data':serializer_data.data},status=status.HTTP_200_OK)
      
      


      




    
    
   

   


   


                 

      
   
      
        
