# Generated by Django 4.1.5 on 2023-07-22 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0088_alter_user_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('supervisor', 'supervisor'), ('student', 'student'), ('fyp_panel', 'fyp_panel'), ('admin', 'admin')], max_length=20, null=True),
        ),
    ]