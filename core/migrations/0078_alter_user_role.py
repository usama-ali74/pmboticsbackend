# Generated by Django 4.1.5 on 2023-06-03 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0077_fyppanel_var'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('supervisor', 'supervisor'), ('student', 'student'), ('fyp_panel', 'fyp_panel'), ('super_admin', 'super_admin')], max_length=20, null=True),
        ),
    ]