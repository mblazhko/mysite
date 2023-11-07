from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.db import models, transaction
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from .models import Poll, Question, Choice, Answer


class IndexView(generic.ListView):
    model = Poll
    template_name = "polls/index.html"
    paginate_by = 10
    queryset = Poll.objects.all()

    def get_context_data(self, **kwargs) -> dict:
        """
        Getting the data for 10 popular Polls based on quantity of answers.
        """
        context = super().get_context_data(**kwargs)
        popular_polls = cache.get("popular_polls")
        if not popular_polls:
            popular_polls = Poll.objects.annotate(
                num_answers=models.Count("question__choice__answer")
            ).order_by("-num_answers")[:10]
        context["popular_polls"] = popular_polls

        return context


class ResultsView(generic.DetailView):
    template_name = "polls/results.html"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """
        Calculate the data for the charts in the result page.
        Check if cached data is available, if not get and cache
        """
        poll = cache.get(f"poll_{kwargs['slug']}")
        if not poll:
            poll = Poll.objects.prefetch_related(
                "question_set__choice_set__answer_set"
            ).get(slug=kwargs["slug"])
            cache.set(f"poll_{kwargs['slug']}", poll)
        questions = poll.question_set.all()

        charts_data = []

        for question in questions:
            labels = [
                choice.choice_text for choice in question.choice_set.all()
            ]
            data = [
                choice.answer_set.count()
                for choice in question.choice_set.all()
            ]

            chart_data = {
                "id": question.id,
                "labels": labels,
                "data": data,
            }

            charts_data.append(chart_data)

        context = {
            "poll": poll,
            "charts_data": charts_data,
        }

        return self.render_to_response(context)


class PollDetailView(LoginRequiredMixin, generic.DetailView):
    model = Poll
    template_name = "polls/poll_detail.html"
    context_object_name = "poll"

    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        context["has_voted"] = (
            Answer.objects.filter(
                owner=self.request.user, choice__question__poll=self.object
            ).exists()
        )
        return context

    def post(self, request, *args, **kwargs) -> HttpResponse:
        poll = self.get_object()
        for question in poll.question_set.all():
            choice_id = request.POST.get(f"choice_{question.id}")
            if choice_id:
                choice = Choice.objects.get(pk=choice_id)
                answer = Answer.objects.filter(
                    choice__question=question, owner=request.user
                ).first()
                if answer:
                    answer.choice = choice
                    answer.save()
                else:
                    Answer.objects.create(choice=choice, owner=request.user)

        return HttpResponseRedirect(
            reverse("polls:poll-results", args=(poll.slug,))
        )


@login_required
def poll_create(request) -> HttpResponse | HttpResponseRedirect:
    """
    View for creating a new poll with at least one question and at least
    two choices for every question.
    All checks located on the frontend side.
    """
    if request.method == "POST":
        name = request.POST.get("title")
        description = request.POST.get("description")

        print(name)
        print(description)

        if name and description:
            with transaction.atomic():
                poll = Poll.objects.create(
                    poll_name=name,
                    poll_description=description,
                    owner=request.user,
                )

                questions = request.POST.getlist("questions")
                for question_text in questions:
                    question = Question.objects.create(
                        poll=poll, question_text=question_text
                    )

                    choices = request.POST.getlist(f"options_{question_text}")
                    for choice_text in choices:
                        Choice.objects.create(
                            question=question, choice_text=choice_text
                        )

                return HttpResponseRedirect(
                    reverse("polls:poll-detail", kwargs={"slug": poll.slug})
                )

    return render(request, "polls/poll_create.html")


@login_required
def poll_delete(request, slug) -> HttpResponse:
    """View to delete a poll"""
    poll = Poll.objects.get(slug=slug)
    poll.delete()

    return HttpResponseRedirect(reverse("custom_user:user_profile"))
