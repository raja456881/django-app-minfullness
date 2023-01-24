from django.urls import path
from .views import *

urlpatterns = [
    path('login', UserLogin.as_view(), name="login POST"),
    path('social_auth', LoginWithSocialAuth.as_view(), name="third party login POST"),
    path('add_user_details', UserDetails.as_view(), name="user details POST"),
    path('profile_details', Profile.as_view(), name="profile POST"),
    path('profile_picture', ProfilePicture.as_view(), name="profile POST"),
]
