# Generated by Django 4.2.16 on 2024-10-18 23:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_imgae_course_slug_course_summary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='course',
            name='summary',
        ),
    ]
