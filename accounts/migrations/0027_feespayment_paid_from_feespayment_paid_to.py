# Generated by Django 4.1.3 on 2022-11-18 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0026_alter_fees_course_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='feespayment',
            name='paid_from',
            field=models.ForeignKey(db_column='paid_from', default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.users'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='feespayment',
            name='paid_to',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
