from django.urls import path

from custom_user.views import update_profile, user_profile

urlpatterns = [
    path("profile/", user_profile, name="user_profile"),
    path("update_profile/", update_profile, name="update_profile"),
]

app_name = "custom_user"
