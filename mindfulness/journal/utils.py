import boto3
from .models import *
from datetime import datetime, timedelta, timezone


def s3_upload_file(file, file_path):
    bucket = 'mindfulness-dev'
    boto3.client('s3', region_name='ap-south-1').upload_fileobj(file, bucket, file_path)
    link = ("https://s3.%s.amazonaws.com/%s/%s" % ("ap-south-1", bucket, file_path)).replace(" ", "+")
    return link


def current_streak(user):
    total_streak = 0
    current_streaks = 0
    today = datetime.now(timezone.utc)
    compare_date = today + timedelta(1)

    entry_dates = list(Journal.objects.values("created_at").filter(user=user, created_at__lte=today).
                       order_by("-created_at"))

    for entry_date in entry_dates:

        for date in entry_date.values():
            delta = compare_date - date
            if delta.days == 1:
                current_streaks += 1
            elif delta.days == 0:
                pass
            else:
                break

        compare_date = date

    if current_streaks > total_streak:
        total_streak = current_streaks

    return total_streak
