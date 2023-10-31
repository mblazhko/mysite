from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.poll_detail, name="poll-detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="poll-results"),
    path("<int:poll_id>/vote/", views.vote, name="vote"),
]

app_name = "polls"
