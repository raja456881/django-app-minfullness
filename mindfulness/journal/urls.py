from django.urls import path
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('all_journal', JournalView.as_view(), name="all journal GET"),
    path('write_journal', JournalWriteView.as_view(), name="write journal POST"),
    path('delete_journal', JournalDeleteView.as_view(), name="delete journal DELETE"),
    path('reminder', ReminderView.as_view(), name="reminder POST"),
    path('all_reminder', AllReminderView.as_view(), name="all reminder POST"),
    path('delete_reminder', ReminderDeleteView.as_view(), name="delete reminder POST"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
