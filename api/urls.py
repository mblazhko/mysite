from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from api.views import PollViewSet, QuestionViewSet


router = routers.DefaultRouter()
router.register("polls", PollViewSet)
router.register("questions", QuestionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "api"
