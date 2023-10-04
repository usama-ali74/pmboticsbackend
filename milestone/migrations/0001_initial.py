# Generated by Django 4.1.5 on 2023-04-30 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0058_merge_20230429_1457'),
    ]

    operations = [
        migrations.CreateModel(
            name='MilestoneWork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, null=True)),
                ('updated_at', models.DateTimeField(blank=True, null=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('document', models.CharField(max_length=255)),
                ('milestone', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, related_name='milestone_work', to='core.milestone')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]