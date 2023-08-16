# Generated by Django 4.1.2 on 2023-08-16 10:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('face_recognition_logic', '0002_alter_student_face_encoding'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='attendance',
            name='student_name',
            field=models.CharField(default=11, max_length=100),
            preserve_default=False,
        ),
    ]