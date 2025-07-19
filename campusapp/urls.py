
from django.urls import path
from .views import *

urlpatterns = [
    path('user-signup/',SignupView.as_view()),
    path('user-login/',LoginView.as_view()),
    path('create-student/',StudentProfileView.as_view()),
    path('add-department/',DepartmentView.as_view()),
    path('add-subject/', SubjectsView.as_view()),
    path('add-semester/',SemesterView.as_view()),
    path('add-faculty/',FacultyView.as_view()),
    path('mark-attendance/',AttendanceView.as_view()),
    path('create-assignment/',AssignmentView.as_view()),
    path('submit-assignment/',AssignmentSubmissionView.as_view()),
    path('view-attendance/',StudentAttendanceView.as_view()),
    path('view-submission/',SubmissionListView.as_view()),


   









]