# Generated by Django 4.1.3 on 2022-11-15 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_alter_tests_option5'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='current_position',
            field=models.TextField(blank=True, null=True),
        ),
    ]