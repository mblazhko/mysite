from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, \
    TokenRefreshView

from api.views import PollViewSet, QuestionViewSet, AnswerViewSet


router = routers.DefaultRouter()
router.register("polls", PollViewSet)
router.register("questions", QuestionViewSet)
router.register("answers", AnswerViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

app_name = "api"
