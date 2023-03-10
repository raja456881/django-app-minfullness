# Generated by Django 4.1.3 on 2022-12-27 12:37

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Journal',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('journal_title', models.CharField(blank=True, max_length=250, null=True)),
                ('journal_text', models.TextField(blank=True, null=True)),
                ('journal_audio', models.CharField(blank=True, max_length=500, null=True)),
                ('journal_image', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=500), blank=True, default=list, null=True, size=None)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('text_to_speech', models.BooleanField(default=True)),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Journal',
            },
        ),
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('reminder_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('reminder_text', models.TextField(blank=True, null=True)),
                ('reminder_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('reminder_on', models.BooleanField(default=True)),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Reminder',
                'unique_together': {('user', 'reminder_id')},
            },
        ),
    ]
