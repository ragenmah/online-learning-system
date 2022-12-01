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


def random_string(size=8, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range( size))


def fileUserpath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('uploads/profiles/', filename)


def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('uploads/courses/', filename)


def filePdfPath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('uploads/resources/', filename)


def filePaymentPath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime('%Y%m%d%H:%M:%S')
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join('uploads/payments/', filename)


class Roles(models.Model):
    ROLES = [
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    ]
    role_title = models.CharField(max_length=100, choices=ROLES)
    role_description = models.CharField(max_length=422, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "roles"


class Users(models.Model):
    user_role_id = models.ForeignKey('Roles', models.DO_NOTHING, db_column='user_role_id')
    name = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to=fileUserpath, null=True, blank=True)
    profile_description = models.TextField(null=True, blank=True)
    current_position = models.TextField(null=True, blank=True)
    email = models.CharField(max_length=200, null=True)
    address = models.CharField(max_length=100, null=True)
    dob = models.DateTimeField(null=True)
    contact_no = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "users"


class Courses(models.Model):
    code = models.SlugField(
        max_length=10,
        default=random_string,
        unique=True, db_column='course_code')
    course_title = models.CharField(max_length=422, blank=False)
    course_description = models.TextField()
    course_thumbnail = models.ImageField(upload_to=filepath, null=True)
    # field_name = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=100, )

    user_id = models.ForeignKey('Users', on_delete=models.CASCADE, db_column='user_id')
    # course_duration_id = models.ForeignKey('Duration', models.DO_NOTHING, db_column='course_duration_id')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

# status
    class Meta:
        db_table = "courses"


class Duration(models.Model):
    duration_time = models.CharField(max_length=422)
    course_id = models.ForeignKey('Courses', on_delete=models.CASCADE, db_column='course_id')
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "durations"


class Resources(models.Model):
    course_id = models.ForeignKey('Courses', on_delete=models.CASCADE, db_column='course_id')
    resource_title = models.CharField(max_length=422, null=True)
    resource_description = models.TextField(null=True)
    resource = models.FileField(upload_to=filePdfPath, null=True)
    resource_type = models.CharField(max_length=10, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "resources"


class Tests(models.Model):
    CORRECT = [
        ('1', 'Option 1'),
        ('2', 'Option 2'),
        ('3', 'Option 3'),
        ('4', 'Option 4'),
        ('5', 'Option 5'),
    ]
    course_id = models.ForeignKey('Courses', on_delete=models.CASCADE, db_column='course_id')
    question = models.TextField( null=True)
    option1 = models.TextField(null=True)
    option2 = models.TextField(null=True)
    option3 = models.TextField(null=True)
    option4 = models.TextField(null=True)
    option5 = models.TextField(null=True, blank=True)
    correct = models.CharField(max_length=100,choices=CORRECT)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "tests"


class Enrolls(models.Model):
    user_id = models.ForeignKey('Users', on_delete=models.CASCADE, db_column='user_id')
    course_id = models.ForeignKey('Courses', on_delete=models.CASCADE, db_column='course_id')
    teacher_id = models.CharField(max_length=422, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "enrolls"


class Fees(models.Model):
    # course_id = models.ForeignKey('Courses', models.DO_NOTHING, db_column='course_id')
    course_id = models.OneToOneField(Courses, on_delete=models.CASCADE, db_column='course_id', blank=True, null=True)
    price = models.IntegerField(null=True, blank=True)
    discount_percentage = models.IntegerField(blank=True, null=True)
    discount_amount = models.CharField(max_length=100, blank=True)
    is_free = models.BooleanField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = "fees"


class FeesPayment(models.Model):
    PAYMENTMDOE = [
        ('Card', 'Card'),
        ('Bank account', 'Bank account'),
    ]
    STATUS = [
        ('1', 'true'),
        ('0', 'false'),
    ]
    course_id = models.ForeignKey('Courses', on_delete=models.CASCADE, db_column='course_id')
    paid_amount = models.IntegerField()
    payment_image = models.ImageField(upload_to=filePaymentPath, null=True)
    payment_method = models.CharField(max_length=100, choices=PAYMENTMDOE)
    status = models.CharField(max_length=100, choices=STATUS)
    paid_from = models.ForeignKey('Users', on_delete=models.CASCADE, db_column='paid_from')
    paid_to = models.CharField(max_length=100,)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        db_table = 'payments'


class ChangePassword(models.Model):
    old_password = models.CharField(max_length=100, blank=True)
    new_password = models.CharField(max_length=100, blank=True)
    retype_password = models.CharField(max_length=100, blank=True)



