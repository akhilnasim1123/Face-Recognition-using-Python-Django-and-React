from django.db import models

# Create your models here.


class RegistrationRequest(models.Model):
    name = models.CharField(max_length=255)
    face_encoding = models.TextField(null=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name