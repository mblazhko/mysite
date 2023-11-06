from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.views import PollViewSet, QuestionViewSet, AnswerViewSet


router = routers.DefaultRouter()
router.register("polls", PollViewSet)
router.register("questions", QuestionViewSet)
router.register("answers", AnswerViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("token/", obtain_auth_token, name="api_token"),
]

app_name = "api"
