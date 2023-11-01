from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    path("", cache_page(60 * 10)(views.IndexView.as_view()), name="index"),
    path("<int:pk>/", views.poll_detail, name="poll-detail"),
    path(
        "<int:pk>/results/", views.ResultsView.as_view(), name="poll-results"
    ),
]

app_name = "polls"
