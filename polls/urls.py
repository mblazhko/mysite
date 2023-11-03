from django.urls import path

from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<slug:slug>/", views.poll_detail, name="poll-detail"),
    path(
        "<slug:slug>/results/", views.ResultsView.as_view(), name="poll-results"
    ),
]

app_name = "polls"
