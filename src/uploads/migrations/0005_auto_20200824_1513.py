# Generated by Django 2.2.14 on 2020-08-24 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0004_video_panopto_session_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='audio',
            name='panopto_session_id',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='audio',
            name='processing_status',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
