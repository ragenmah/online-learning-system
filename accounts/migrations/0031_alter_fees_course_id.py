# Generated by Django 4.1.3 on 2022-11-24 12:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0030_alter_fees_course_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fees',
            name='course_id',
            field=models.OneToOneField(blank=True, db_column='course_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.courses'),
        ),
    ]