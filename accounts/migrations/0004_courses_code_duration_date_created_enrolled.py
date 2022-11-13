# Generated by Django 4.1.3 on 2022-11-11 10:38

import accounts.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_courses_roles_date_created_users_date_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='courses',
            name='code',
            field=models.SlugField(default=accounts.models.random_string, max_length=10, unique=True),
        ),
        migrations.AddField(
            model_name='duration',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.CreateModel(
            name='Enrolled',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('course', models.ForeignKey(db_column='course_id', on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.courses')),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.users')),
            ],
        ),
    ]
