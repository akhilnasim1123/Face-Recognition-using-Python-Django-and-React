from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=100)
    face_encoding = models.TextField()  # Use TextField instead of BinaryField

    def __str__(self):
        return self.name



class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField(auto_now_add=False,null=True)
    check_out_time = models.DateTimeField(auto_now_add=False,null=True)


