# Generated by Django 4.2.16 on 2024-10-18 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_remove_course_slug_remove_course_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='slug',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='course',
            name='summary',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
