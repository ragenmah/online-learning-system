# Generated by Django 4.1.3 on 2022-11-13 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_courses_user_id_alter_roles_role_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='course_thumbnail',
            field=models.ImageField(default=1, upload_to='images/'),
            preserve_default=False,
        ),
    ]