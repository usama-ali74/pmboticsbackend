# Generated by Django 4.1.5 on 2023-04-11 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_alter_teammember_enrollmentno_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='supervisor',
            name='name',
        ),
    ]