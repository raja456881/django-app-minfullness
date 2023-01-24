import jwt
from .models import *
from firebase_admin import auth
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from journal.utils import *


# Create your views here.
class UserLogin(APIView):

    @staticmethod
    def post(request):
        id_token = request.data['id_token']
        fcm_token = request.data['fcm_token']
        decoded_token = auth.verify_id_token(id_token)
        phone = decoded_token['phone_number']
        user_exists = False
        user = User.objects.filter(phone=phone)

        if user:
            '''if user already exists'''
            user_exists = True
            user = User.objects.get(phone=phone)
            '''checking fcm token in db'''
            if user.fcm_token is None:
                user.fcm_token = []
                user.fcm_token.append(*fcm_token)
                user.save()
            else:
                '''if fcm token is new, add in the db'''
                if fcm_token[0] not in user.fcm_token:
                    user.fcm_token.append(*fcm_token)
                    user.save()
            refresh = RefreshToken.for_user(user)
            return Response({'user_exists': user_exists,
                             'status': status.HTTP_200_OK,
                             'refresh': str(refresh),
                             'access': str(refresh.access_token)})
        else:
            '''creating new user and updating db'''
            User.objects.create(phone=phone)
            user = User.objects.get(phone=phone)
            user.fcm_token = fcm_token
            user.username = phone
            user.save()
            '''generating JWT token'''
            refresh = RefreshToken.for_user(user)
            return Response({'user_exists': user_exists,
                             'status': status.HTTP_200_OK,
                             'refresh': str(refresh),
                             'access': str(refresh.access_token)})


class LoginWithSocialAuth(APIView):

    @staticmethod
    def post(request):
        id_token = request.data['id_token']
        fcm_token = request.data['fcm_token']
        decoded_token = jwt.decode(id_token, options={"verify_signature": False})
        email = decoded_token['email']
        user_exists = False
        user = User.objects.filter(email=email)
        if user:
            '''if user already exists'''
            user_exists = True
            user = User.objects.get(email=email)
            '''checking fcm token in db'''
            if user.fcm_token is None:
                user.fcm_token = []
                user.fcm_token.append(*fcm_token)
                user.save()
            else:
                '''if fcm token is new, add in the db'''
                if fcm_token[0] not in user.fcm_token:
                    user.fcm_token.append(*fcm_token)
                    user.save()
            refresh = RefreshToken.for_user(user)
            return Response({'user_exists': user_exists,
                             'status': status.HTTP_200_OK,
                             'refresh': str(refresh),
                             'access': str(refresh.access_token)})
        else:
            '''creating new user and updating db'''
            User.objects.create(email=email)
            user = User.objects.get(email=email)
            user.fcm_token = fcm_token
            user.username = email
            user.save()

            '''generating JWT token'''
            refresh = RefreshToken.for_user(user)
            return Response({'user_exists': user_exists,
                             'status': status.HTTP_200_OK,
                             'refresh': str(refresh),
                             'access': str(refresh.access_token)})


class UserDetails(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = self.request.user
        curr_user = User.objects.get(username=user)

        serializer = UserDetailsSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        '''getting validated data through serializer'''
        curr_user.full_name = serializer.validated_data.get('full_name')
        curr_user.gender = serializer.validated_data.get('gender')
        curr_user.date_of_birth = serializer.validated_data.get('date_of_birth')
        curr_user.save()
        return Response({'status': status.HTTP_200_OK,
                         'data': serializer.data})


class Profile(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user
        curr_user = User.objects.get(username=user)
        user = ProfileSerializer(curr_user, context={'request': request})
        return Response({'success': status.HTTP_200_OK,
                         'data': user.data})


class ProfilePicture(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = self.request.user
        curr_user = User.objects.get(username=user)

        picture = request.FILES['picture']
        curr_user.picture = picture
        curr_user.save()
        serializer = ProfilePictureSerializer(curr_user, context={'request': request})

        return Response({'success': status.HTTP_200_OK,
                         'data': serializer.data})
