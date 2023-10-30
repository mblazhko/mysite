from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.views.generic.edit import FormMixin

from polls.forms import PollForm
from polls.models import Question, Choice, Poll, Answer


class IndexView(generic.ListView):
    model = Poll
    template_name = "polls/index.html"
    queryset = Poll.objects.all()


class DetailView(generic.DetailView):
    model = Poll
    template_name = "polls/poll_detail.html"
    form_class = PollForm


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
