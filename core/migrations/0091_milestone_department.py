# Generated by Django 4.1.5 on 2023-07-24 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0090_alter_department_uni'),
    ]

    operations = [
        migrations.AddField(
            model_name='milestone',
            name='department',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='core.department'),
        ),
    ]