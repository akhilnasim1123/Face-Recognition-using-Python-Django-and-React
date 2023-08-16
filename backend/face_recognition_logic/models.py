from django.db import models
from datetime import date

class Student(models.Model):
    name = models.CharField(max_length=100)
    face_encoding = models.TextField()

    def __str__(self):
        return self.name



class Attendance(models.Model):
    date = models.DateField(default=date.today)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    check_in_time = models.DateTimeField(null=True)
    check_out_time = models.DateTimeField(null=True)


