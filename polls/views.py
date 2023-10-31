from django.db import models
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.views.decorators.cache import cache_page

from polls.models import Choice, Poll, Answer


class IndexView(generic.ListView):
    model = Poll
    template_name = "polls/index.html"
    paginate_by = 10
    queryset = Poll.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        popular_polls = Poll.objects.annotate(num_answers=models.Count('question__choice__answer')).order_by('-num_answers')[:10]
        context["popular_polls"] = popular_polls

        return context


@cache_page(timeout=60 * 30)
def poll_detail(request, pk):
    poll = get_object_or_404(Poll, pk=pk)

    if request.method == 'POST':
        for question in poll.question_set.all():
            choice_id = request.POST.get(f'choice_{question.id}')
            if choice_id:
                choice = Choice.objects.get(pk=choice_id)
                Answer.objects.create(choice=choice)

        return HttpResponseRedirect(
            reverse('polls:poll-results', args=(poll.id,)))

    return render(request, 'polls/poll_detail.html', {'poll': poll})


class ResultsView(generic.DetailView):
    model = Poll
    template_name = "polls/results.html"


def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.method == 'POST':
        form = PollForm(request.POST)
        if form.is_valid():
            selected_choice = form.cleaned_data['choice']
            Answer.objects.create(choice=selected_choice, answer_text=selected_choice.choice_text)
            return HttpResponseRedirect(reverse('polls:results', args=(poll.id,)))
    else:
        form = PollForm(initial={'poll_name': poll.poll_name})
    return render(request, 'polls/vote.html', {'form': form, 'poll': poll})
