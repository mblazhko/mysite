from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db import models
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from polls.models import Choice, Poll, Answer


class IndexView(generic.ListView):
    model = Poll
    template_name = "polls/index.html"
    paginate_by = 10
    queryset = Poll.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        popular_polls = Poll.objects.annotate(
            num_answers=models.Count("question__choice__answer")
        ).order_by("-num_answers")[:10]
        context["popular_polls"] = popular_polls

        return context


@login_required
def poll_detail(request, pk) -> HttpResponse:
    poll = Poll.objects.prefetch_related(
        "question_set__choice_set__answer_set"
    ).get(pk=pk)
    user = request.user
    has_voted = Answer.objects.filter(owner=user, choice__question__poll=poll).exists()

    if request.method == "POST":
        for question in poll.question_set.all():
            choice_id = request.POST.get(f"choice_{question.id}")
            if choice_id:
                choice = Choice.objects.get(pk=choice_id)
                answer = Answer.objects.filter(
                    choice__question=question, owner=user).first()
                if answer:
                    answer.choice = choice
                    answer.save()
                else:
                    Answer.objects.create(choice=choice,
                                          owner=user)

        return HttpResponseRedirect(
            reverse("polls:poll-results", args=(poll.id,))
        )

    return render(request, "polls/poll_detail.html", {"poll": poll, "has_voted": has_voted})


class ResultsView(generic.DetailView):
    template_name = "polls/results.html"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        poll = cache.get(f"poll_{kwargs['pk']}")
        if not poll:
            poll = Poll.objects.prefetch_related(
                "question_set__choice_set__answer_set"
            ).get(pk=kwargs["pk"])
            cache.set(f"poll_{kwargs['pk']}", poll)
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
