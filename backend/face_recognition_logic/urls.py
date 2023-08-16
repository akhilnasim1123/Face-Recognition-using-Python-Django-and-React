from django.urls import path
from .views import MarkAttendance, StudentList,CheckOut

urlpatterns = [
    path('api/mark-attendance/', MarkAttendance.as_view(), name='mark-attendance'),
    path('api/attendance-checkout/',CheckOut.as_view()),
    path('api/students/', StudentList.as_view(), name='student-list'),
]