import datetime as dt

import pytz
from dateutil.tz import tzutc

from .models import *
from .utils import *
from datetime import datetime
import datetime
from datetime import datetime
from rest_framework import serializers


class JournalPostSerializer(serializers.ModelSerializer):
    local_time = serializers.SerializerMethodField()

    class Meta:
        model = Journal
        fields = ['id', 'journal_title', 'journal_text', 'journal_audio', 'journal_image', 'created_at', 'local_time']

    def get_local_time(self, instance):
        local_timezone = pytz.timezone('Asia/Kolkata')
        local_time = instance.created_at.astimezone(local_timezone)
        return local_time


class ReminderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reminder
        fields = '__all__'
