# Generated by Django 4.1.5 on 2023-06-17 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0081_university_alter_department_name_department_uni'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='uni',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='University', to='core.university'),
        ),
    ]
