from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import CharField
from django.urls import reverse
from django.utils import timezone, text
from django.core.validators import MaxValueValidator, MinValueValidator
import os
import datetime
import random
import string

def _(something):
    return something

class User(AbstractUser):
    is_student = models.BooleanField('student status', default=False)
    is_teacher = models.BooleanField('teacher status', default=False)


class Roles(models.Model):
    ROLES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    role_title = models.CharField(max_length=100,choices=ROLES)
    role_description = models.CharField(max_length=422)
    date_created = models.DateTimeField(auto_now_add=True, null=True )

    class Meta:
        db_table = "roles"

class Users(models.Model):
    user_role_id = models.ForeignKey('Roles', models.DO_NOTHING, db_column='user_role_id')
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=100, null=True)
    dob = models.DateTimeField(null=True)
    contact_no = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "users"


def random_string(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range( size))

class Courses(models.Model):
    code = models.SlugField(
        max_length=10,
        default=random_string,
        unique=True, db_column='course_code')
    course_title = models.CharField(max_length=422, blank=False)
    course_description = models.CharField(max_length=422)
    user_id= models.ForeignKey('Users', models.DO_NOTHING, db_column='user_id')
    # course_duration_id = models.ForeignKey('Duration', models.DO_NOTHING, db_column='course_duration_id')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "courses"



class Duration(models.Model):
    duration_time = models.CharField(max_length=422)
    course_id = models.ForeignKey('Courses', models.DO_NOTHING, db_column='course_id')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "durations"

class Enrolled(models.Model):
    user = models.ForeignKey('Users',models.DO_NOTHING, db_column='user_id')
    course = models.ForeignKey('Courses', models.DO_NOTHING, db_column='course_id')
    date_created = models.DateTimeField(auto_now_add=True, null=True)


# class Fees(models.Model):
#     user = models.ForeignKey('Users',models.DO_NOTHING, db_column='user_id')
#     course_id = models.ForeignKey('Courses', models.DO_NOTHING, db_column='course_id')
#     date_created = models.DateTimeField(auto_now_add=True, null=True)
#
#     class Meta:
#         db_table = "fees"




# enrolled table needed?
# buttton for course complete
# give test
# test result
