# Generated by Django 4.1.3 on 2022-11-14 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_alter_courses_course_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courses',
            name='course_thumbnail',
            field=models.ImageField(null=True, upload_to='images/course_images/'),
        ),
    ]