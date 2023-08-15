from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import RegistrationRequest
from .serializers import RegistrationRequestSerializer
from rest_framework.permissions import IsAuthenticated
import face_recognition 
import numpy as np
from PIL import Image
import io
import base64

class RegistrationRequestView(APIView):
    def post(self, request):
        name = request.data.get('name')
        image_data = request.data.get('image')

        if not name or not image_data:
            return Response({'error': 'Name and image data are required.'}, status=status.HTTP_400_BAD_REQUEST)

        face_encoding = encode_face(image_data)
        if face_encoding is None:
            return Response({'error': 'No face found in the image.'}, status=status.HTTP_400_BAD_REQUEST)

        face_encoding_text = ','.join(map(str, face_encoding.tolist()))

        request_instance = RegistrationRequest(name=name, face_encoding=face_encoding_text)
        request_instance.save()

        return Response({'message': 'Registration request sent successfully.'}, status=status.HTTP_201_CREATED)


    def get(self, request):
        requests = RegistrationRequest.objects.all()
        serializer = RegistrationRequestSerializer(requests, many=True)
        return Response(serializer.data)

def encode_face(image_data):
    try:
        image_data_decoded = base64.b64decode(image_data.split(',')[1])
        image = Image.open(io.BytesIO(image_data_decoded))
        face_encodings = face_recognition.face_encodings(np.array(image.convert('RGB')))

        if len(face_encodings) == 0:
            return None

        face_encoding = face_encodings[0]

        # Convert the face encoding to base64 with correct padding
        face_encoding_base64 = base64.b64encode(face_encoding.tobytes()).decode()

        return face_encoding_base64
    except IndexError:
        return None

