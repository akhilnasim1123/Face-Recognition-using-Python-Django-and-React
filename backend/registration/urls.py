from django.urls import path
from .views import RegistrationRequestView


urlpatterns = [
path('registration-requests/', RegistrationRequestView.as_view(), name='registration-requests'),
]