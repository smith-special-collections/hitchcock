# Generated by Django 2.2.14 on 2020-08-24 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0002_video_processing_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='upload',
            name='queued_for_processing',
            field=models.BooleanField(default=False),
        ),
    ]