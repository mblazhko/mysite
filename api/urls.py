from django.urls import path, include
from rest_framework import routers
from api.views import PollViewSet, QuestionViewSet, ChoiceViewSet, AnswerViewSet


router = routers.DefaultRouter()
router.register("polls", PollViewSet)
router.register("questions", QuestionViewSet)
router.register("answers", AnswerViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "api"
