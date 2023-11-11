from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import generic

from .models import Answer, Choice, Poll, Question
from .utils.cache_utils import get_popular_polls_cache, get_cached_poll, \
    get_cached_charts_data, get_has_voted_cache


class IndexView(generic.ListView):
    """List of all available Polls"""

    model = Poll
    template_name = "polls/index.html"
    paginate_by = 10
    queryset = Poll.objects.all()

    def get_context_data(self, **kwargs) -> dict:
        """
        Getting the data for 10 popular Polls based on quantity of answers.
        """
        context = super().get_context_data(**kwargs)
        context["popular_polls"] = get_popular_polls_cache()

        return context


class ResultsView(generic.DetailView):
    template_name = "polls/poll_results.html"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """
        Calculate the data for the charts in the result page.
        Check if cached data is available, if not get and cache
        """
        poll = get_cached_poll(kwargs["slug"])
        charts_data = get_cached_charts_data(poll=poll)

        context = {
            "poll": poll,
            "charts_data": charts_data,
        }

        return self.render_to_response(context)


class PollDetailView(LoginRequiredMixin, generic.DetailView):
    """Detail view for Poll and possibility to vote"""

    model = Poll
    template_name = "polls/poll_detail.html"

    def get_context_data(self, **kwargs) -> dict:
        """Get data if user already has voted"""
        context = super().get_context_data(**kwargs)
        context["questions"] = Question.objects.prefetch_related(
            "choice_set"
        ).filter(poll=self.object)
        context["has_voted"] = get_has_voted_cache(
            user=self.request.user,
            poll=self.get_object()
        )
        return context

    def post(self, request, *args, **kwargs) -> HttpResponse:
        """
        Vote and assign answers to user.
        Re-vote if user already has voted.
        """
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


class PollCreateView(LoginRequiredMixin, generic.CreateView):
    """
    View for creating a new poll with at least one question and at least
    two choices for every question.
    All checks located on the frontend side.
    """

    model = Poll
    template_name = "polls/poll_create.html"

    def post(self, request, *args, **kwargs) -> HttpResponse:
        """
        Create a new poll using data from the post-request
        """
        name = request.POST.get("title")
        description = request.POST.get("description")

        if name and description:
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

    def get(self, request, *args, **kwargs) -> HttpResponse:
        return render(request, self.template_name)


class PollDeleteView(LoginRequiredMixin, generic.DeleteView):
    """View to delete the poll"""

    model = Poll
    success_url = reverse_lazy("custom_user:user_profile")
