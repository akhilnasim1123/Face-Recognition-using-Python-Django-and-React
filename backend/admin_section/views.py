from django.contrib.auth import authenticate, login
import numpy as np
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from registration.serializers import RegistrationRequestSerializer
from face_recognition_logic.serializers import StudentSerializer,AttendanceSerializer
from registration.models import RegistrationRequest
from face_recognition_logic.models import Student, Attendance
import base64
@api_view(['POST'])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user:
        login(request, user)
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    



@api_view(['GET'])
def get_students(request):
    students = Student.objects.all()
    print(students)
    serializer = StudentSerializer(students, many=True)
    return Response({'students': serializer.data})

@api_view(['GET'])
def get_registration_requests(request):
    requests = RegistrationRequest.objects.all()
    print(request)
    serializer = RegistrationRequestSerializer(requests, many=True)
    return Response({'registrationRequests': serializer.data})

@api_view(['POST'])
def approve_registration_request(request, request_id):
    try:
        registration_request = RegistrationRequest.objects.get(pk=request_id)
        registration_request.approved = True
        registration_request.save()
    except RegistrationRequest.DoesNotExist:
        return Response({'error': 'Registration request not found.'}, status=status.HTTP_404_NOT_FOUND)

    print("Debug: Registration request approved. Request ID:", request_id)
    print("Debug: Registration request face_encoding:", registration_request.face_encoding)

    student_data = {
        'name': registration_request.name,
        'face_encoding': registration_request.face_encoding  # Assuming it's already a string
    }

    serializer = StudentSerializer(data=student_data)
    if serializer.is_valid():
        serializer.save()
        print("Debug: Student data saved successfully.")
        registration_request.delete()
        return Response({'message': 'Registration request approved.'}, status=status.HTTP_200_OK)
    else:
        print("Debug: Student data validation failed:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def ignore_registration_request(request, request_id):
    try:
        registration_request = RegistrationRequest.objects.get(pk=request_id)
    except RegistrationRequest.DoesNotExist:
        return Response({'error': 'Registration request not found.'}, status=status.HTTP_404_NOT_FOUND)

    registration_request.delete()
    return Response({'message': 'Registration request ignored.'}, status=status.HTTP_200_OK)

class AttendanceReportAPIView(APIView):
    def get(self, request, *args, **kwargs):
        attendance_entries = Attendance.objects.all()
        serializer = AttendanceSerializer(attendance_entries, many=True)
        return Response({'attendanceReport': serializer.data})