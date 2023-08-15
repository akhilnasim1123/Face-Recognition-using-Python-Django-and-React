from django import views
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='admin-login'),
    # path('api/students/', StudentList.as_view(), name='student-list'),
    path('students/', views.get_students),
    path('registration-requests/', views.get_registration_requests),
    path('approve-request/<int:request_id>/', views.approve_registration_request),
    path('ignore-request/<int:request_id>/', views.ignore_registration_request),
    path('attendance-report/', views.AttendanceReportAPIView.as_view(), name='attendance-report'),

]