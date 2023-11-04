from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("poll-<slug:slug>/", views.poll_detail, name="poll-detail"),
    path(
        "poll-<slug:slug>/results/", views.ResultsView.as_view(), name="poll-results"
    ),
    path('create-poll/', views.poll_create, name='poll-create'),
]

app_name = "polls"
