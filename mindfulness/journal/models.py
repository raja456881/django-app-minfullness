import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import now
from accounts.models import User
from django.contrib.postgres.fields import ArrayField


def nameFile(instance, filename):
    return '/'.join(['media', str(instance.id), filename])


class Journal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    journal_title = models.CharField(max_length=250, null=True, blank=True)
    journal_text = models.TextField(null=True, blank=True)
    journal_audio = models.CharField(max_length=500, null=True, blank=True)
    journal_image = ArrayField(models.CharField(max_length=500), default=list, null=True, blank=True)
    created_at = models.DateTimeField(default=now)
    text_to_speech = models.BooleanField(default=True)

    class Meta:
        db_table = 'Journal'

    def __str__(self):
        return str(self.user)


class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    reminder_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    reminder_text = models.TextField(null=True, blank=True)
    reminder_time = models.DateTimeField(default=timezone.now)
    reminder_on = models.BooleanField(default=True)

    class Meta:
        db_table = 'Reminder'
        unique_together = ['user', 'reminder_id']
