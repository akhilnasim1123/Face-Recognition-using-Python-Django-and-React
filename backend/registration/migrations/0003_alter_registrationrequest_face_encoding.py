# Generated by Django 4.1.2 on 2023-08-15 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_alter_registrationrequest_face_encoding'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationrequest',
            name='face_encoding',
            field=models.TextField(null=True),
        ),
    ]
