# Generated by Django 2.2.14 on 2020-08-13 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0007_auto_20200813_1416'),
    ]

    operations = [
        migrations.CreateModel(
            name='VideoVttTrack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload', models.FileField(help_text='vtt format only', max_length=1024, upload_to='text/vtt/')),
                ('type', models.CharField(choices=[('captions', 'Captions (for hearing impairment)'), ('subtitles', 'Subtitles (for language translations)'), ('descriptions', 'Descriptions (for vision impairment)')], max_length=16)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uploads.Video')),
            ],
        ),
    ]