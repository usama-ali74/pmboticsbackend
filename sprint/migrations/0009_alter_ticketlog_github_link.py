# Generated by Django 4.1.5 on 2023-06-16 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sprint', '0008_ticketlog_github_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketlog',
            name='github_link',
            field=models.CharField(max_length=255),
        ),
    ]
