# Generated by Django 4.1.5 on 2023-04-28 15:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0051_remove_milestone_fyp_panel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='core.department'),
        ),
    ]
