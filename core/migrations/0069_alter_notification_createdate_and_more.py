# Generated by Django 4.1.5 on 2023-05-10 09:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0068_notification_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='createdate',
            field=models.DateField(default=datetime.date(2023, 5, 10)),
        ),
        migrations.AlterField(
            model_name='notification',
            name='createtime',
            field=models.TimeField(default='14:27'),
        ),
    ]
