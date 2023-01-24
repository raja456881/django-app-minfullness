from django.contrib import admin
from .models import *


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    list_filter = ('created_at',)


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('user', 'reminder_time')
    list_filter = ('reminder_time',)

    def has_add_permission(self, request):
        objects = self.model.objects.count()
        if objects >= 3:
            return False
        else:
            return True
