from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import face_recognition 
import numpy as np
from .models import Student, Attendance
from django.core.files.base import ContentFile
import base64
from PIL import Image
import io
from .serializers import *

class MarkAttendance(APIView):
    def post(self, request):
        image_data = request.data.get('image')
        if not image_data:
            return Response({'error': 'Image Data is Required'}, status=status.HTTP_400_BAD_REQUEST)

        image_data_decoded = base64.b64decode(image_data.split(',')[1])

        image = Image.open(io.BytesIO(image_data_decoded))

        face_encodings = face_recognition.face_encodings(np.array(image))
        if len(face_encodings) == 0:
            return Response({'error': 'No face found in the image.'}, status=status.HTTP_400_BAD_REQUEST)
        student_face_encoding = face_encodings[0] 

        students = Student.objects.exclude(face_encoding__isnull=True)

        for student in students:
            try:
                decoded_face_encoding = base64.b64decode(student.face_encoding.encode())
                print("Decoded face encoding:", decoded_face_encoding)
            except Exception as e:
                print("Error decoding face encoding for student:", student.id, e)

        student_face_encodings_np = [np.frombuffer(base64.b64decode(s.face_encoding.encode()), dtype=np.float64) for s in students]

        matches = face_recognition.compare_faces(student_face_encodings_np, student_face_encoding)
        if True in matches:
            matched_student = students[matches.index(True)]
            today = timezone.now().date()
            existing_attendance = Attendance.objects.filter(student=matched_student, date=today).first()

            if existing_attendance:
                if existing_attendance.check_in_time:
                    return Response({'message': 'Already checked in.'}, status=status.HTTP_200_OK)
                else:
                    existing_attendance.check_in_time = timezone.now()
                    existing_attendance.save()
                    return Response({'message': 'Check-in marked successfully.'}, status=status.HTTP_200_OK)
            else:
                new_attendance = Attendance(student=matched_student, date=today, check_in_time=timezone.now())
                new_attendance.save()

                matched_student.face_encoding = student_face_encoding.tostring()
                matched_student.save()

                return Response({'message': 'Check-in marked successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No matching student found.'}, status=status.HTTP_404_NOT_FOUND)


class CheckOut(APIView):
    def post(self, request):
        image_data = request.data.get('image')
        if not image_data:
            return Response({'error': 'Image Data is Required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            image_data_decoded = base64.b64decode(image_data.split(',')[1])
            image = Image.open(io.BytesIO(image_data_decoded))
            student_face_encoding = face_recognition.face_encodings(np.array(image))[0]
        except IndexError:
            return Response({'error': 'No face found in the image.'}, status=status.HTTP_400_BAD_REQUEST)
        
        students = Student.objects.all()
        matches = face_recognition.compare_faces([np.fromstring(s.face_encoding) for s in students], student_face_encoding)
        
        if True in matches:
            matched_student = students[matches.index(True)]
            existing_attendance = Attendance.objects.filter(student=matched_student).first()
            
            if existing_attendance:
                if existing_attendance.check_out_time:
                    return Response({'message': 'Already checked out.'}, status=status.HTTP_200_OK)
                else:
                    # Mark check-out time
                    existing_attendance.check_out_time = timezone.now()
                    existing_attendance.save()
                    return Response({'message': 'Check-out marked successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Attendance not marked yet. Mark attendance first.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'No matching student found.'}, status=status.HTTP_404_NOT_FOUND)
class StudentList(APIView):
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
