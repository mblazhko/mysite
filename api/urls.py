from django.urls import include, path
from rest_framework import routers

from api.views import PollViewSet, QuestionViewSet

router = routers.DefaultRouter()
router.register("polls", PollViewSet)
router.register("questions", QuestionViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "api"
