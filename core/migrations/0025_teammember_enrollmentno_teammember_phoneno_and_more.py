# Generated by Django 4.1.5 on 2023-04-11 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_remove_supervisor_department'),
    ]

    operations = [
        migrations.AddField(
            model_name='teammember',
            name='enrollmentno',
            field=models.CharField(default=False, max_length=50, unique=True),
        ),
        migrations.AddField(
            model_name='teammember',
            name='phoneno',
            field=models.CharField(default=False, max_length=50, unique=True),
        ),
        migrations.AddField(
            model_name='teammember',
            name='seatno',
            field=models.CharField(default=False, max_length=50, unique=True),
        ),
    ]
