from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

from polls.models import Poll


@login_required
def user_profile(request) -> HttpResponse:
    """Profile view with showing the polls created by user"""
    user = request.user
    user_polls = Poll.objects.filter(owner=user).select_related("owner")
    return render(request, "user/profile.html", context={"polls": user_polls})


@login_required
def update_profile(request) -> HttpResponseRedirect:
    """View for updating user's first name and last name"""
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        if first_name and last_name:
            user = request.user
            user.first_name = first_name
            user.last_name = last_name
            user.save()
    return redirect("custom_user:user_profile")
