from .models import Journal
from accounts.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .utils import *


# Create your views here.
class JournalView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user
        curr_user = User.objects.get(username=user)

        '''getting queryset of requested date by user'''
        journal = Journal.objects.filter(user=curr_user)

        '''using streak function from utils.py'''
        streak = current_streak(curr_user)

        '''serializing data and sending it as response'''
        serializer = JournalPostSerializer(journal, many=True)

        return Response({'status': status.HTTP_200_OK,
                         'data': serializer.data,
                         'streak': streak})


class JournalWriteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = self.request.user
        curr_user = User.objects.get(username=user)

        journal_title = request.data['journal_title']
        text_to_speech = request.data['text_to_speech']
        journal_text = request.data['journal_text']
        try:
            journal_audio = request.FILES['journal_audio']
            audio = s3_upload_file(journal_audio, f'media/{str(journal_audio)}')
        except BaseException:
            audio = None

        '''getting multiple images'''
        journal_image = request.FILES.getlist('journal_image')
        images = []

        '''uploading audio and image to s3 bucket, creating s3 url'''
        for image in journal_image:
            converted_string = str(image)
            pic = s3_upload_file(image, f'media/{converted_string}')
            images.append(pic)

        '''creating entry of a journal in db'''
        journal = Journal.objects.create(user=curr_user, journal_title=journal_title, journal_text=journal_text,
                                         journal_audio=audio, journal_image=images, text_to_speech=text_to_speech)

        '''serializing the data'''
        serializer = JournalPostSerializer(journal)
        return Response({'status': status.HTTP_200_OK,
                         'data': serializer.data})


class JournalDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        journal_id = request.data['journal_id']

        '''filtering journal according to the id'''
        journal = Journal.objects.filter(id=journal_id)

        '''deleting the journal from db'''
        journal.delete()

        return Response({'status': status.HTTP_200_OK,
                         'data': 'Journal deleted successfully'})


class ReminderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = self.request.user
        curr_user = User.objects.get(username=user)

        reminder_text = request.data['reminder_text']
        reminder_time = request.data['reminder_time']
        reminder_on = request.data['reminder_on']

        reminder = Reminder.objects.create(user=curr_user, reminder_time=reminder_time,
                                           reminder_text=reminder_text, reminder_on=reminder_on)

        serializer = ReminderSerializer(reminder)

        return Response({'status': status.HTTP_200_OK,
                         'data': serializer.data})


class AllReminderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user
        curr_user = User.objects.get(username=user)

        '''getting queryset of requested date by user'''
        reminder = Reminder.objects.filter(user=curr_user)

        '''serializing data and sending it as response'''
        serializer = ReminderSerializer(reminder, many=True)

        return Response({'status': status.HTTP_200_OK,
                         'data': serializer.data})


class ReminderDeleteView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        reminder_id = request.data['reminder_id']

        '''filtering reminder according to the id'''
        reminder = Reminder.objects.filter(id=reminder_id)

        '''deleting the reminder from db'''
        reminder.delete()

        return Response({'status': status.HTTP_200_OK,
                         'data': 'Reminder deleted successfully'})

