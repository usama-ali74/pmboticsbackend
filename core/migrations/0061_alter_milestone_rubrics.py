# Generated by Django 4.1.5 on 2023-05-02 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0060_alter_milestone_marks_alter_milestone_rubrics'),
    ]

    operations = [
        migrations.AlterField(
            model_name='milestone',
            name='rubrics',
            field=models.JSONField(),
        ),
    ]
