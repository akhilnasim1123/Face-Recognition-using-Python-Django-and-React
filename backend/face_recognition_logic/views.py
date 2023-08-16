import binascii
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
from datetime import datetime
import base64

def decode_padded_base64(s):
    try:
        s = s.rstrip('=')
        padding = '=' * (4 - len(s) % 4)
        padded_s = s + padding

        decoded_data = np.frombuffer(base64.b64decode(padded_s), dtype=np.float64)
        return decoded_data
    except Exception as e:
        print("Error decoding base64:", e)
        return np.array([])



class MarkAttendance(APIView):
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
        
        students = Student.objects.exclude(face_encoding__isnull=True)

        student_face_encodings_db = [s.face_encoding for s in students]
        student_face_encodings = [decode_padded_base64(encoding) for encoding in student_face_encodings_db]

        # Remove face encodings with inconsistent shapes
        student_face_encodings = [enc for enc in student_face_encodings if len(enc) == len(student_face_encoding)]

        print("Debug: Number of students:", len(students))
        print("Debug: Decoded student face encodings:", student_face_encodings)
        
        # Perform face recognition
        matches = face_recognition.compare_faces(student_face_encodings, student_face_encoding)

        if True in matches:
            matched_student = students[matches.index(True)]
            today = timezone.now()
            current_date = datetime.now().date()

            existing_attendance = Attendance.objects.filter(student=matched_student, check_in_time__date=today).first()
            student_name_of = Student.objects.get(name=matched_student)
            print(student_name_of.name)
            if existing_attendance:
                if existing_attendance.check_in_time:
                    return Response({'message': 'Already checked in.'}, status=status.HTTP_200_OK)
                else:
                    existing_attendance.check_in_time = timezone.now()
                    existing_attendance.save()
                    return Response({'message': 'Check-in marked successfully.', 'student_id': matched_student.id, 'student_name': matched_student.name}, status=status.HTTP_200_OK)
            else:

                new_attendance = Attendance(student=matched_student,student_name = student_name_of.name, check_in_time=timezone.now())
                new_attendance.save()

                matched_student.face_encoding = base64.b64encode(student_face_encoding.tobytes()).decode()
                matched_student.save()

                return Response({'message': 'Check-in marked successfully.', 'student_id': matched_student.id, 'student_name': matched_student.name}, status=status.HTTP_200_OK)
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
        
        students = Student.objects.exclude(face_encoding__isnull=True)

        student_face_encodings_np = [decode_padded_base64(s.face_encoding) for s in students if s.face_encoding]
        student_face_encodings_np = [enc for enc in student_face_encodings_np if len(enc) == 128] 

        print("Debug: Number of students:", len(students))
        print("Debug: Decoded student face encodings:", student_face_encodings_np)

        matches = face_recognition.compare_faces(student_face_encodings_np, student_face_encoding)
        print("Debug: Matches:", matches)
        
        if True in matches:
            matched_student = students[matches.index(True)]
            existing_attendance = Attendance.objects.filter(student=matched_student).first()
            
            if existing_attendance:
                if existing_attendance.check_out_time:
                    return Response({'message': 'Already checked out.'}, status=status.HTTP_200_OK)
                else:
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
