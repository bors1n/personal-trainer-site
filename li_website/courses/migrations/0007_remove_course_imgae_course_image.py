# Generated by Django 4.2.16 on 2024-10-19 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_course_imgae_course_slug_course_summary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='imgae',
        ),
        migrations.AddField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, upload_to='courses/images/'),
        ),
    ]