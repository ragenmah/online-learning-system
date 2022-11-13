# Generated by Django 4.1.3 on 2022-11-12 11:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_courses_course_duration_id_alter_courses_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='user_id',
            field=models.ForeignKey(db_column='user_id', default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.users'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='roles',
            name='role_title',
            field=models.CharField(choices=[('admin', 'Admin'), ('teacher', 'Teacher'), ('student', 'Student')], max_length=100),
        ),
    ]
