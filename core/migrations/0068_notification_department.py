# Generated by Django 4.1.5 on 2023-05-10 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0067_alter_notification_createdby'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='core.department'),
        ),
    ]
