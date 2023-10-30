from django import forms

from polls.models import Poll, Question, Choice


class PollForm(forms.ModelForm):
    choice = forms.ModelChoiceField(queryset=Choice.objects.all(), widget=forms.RadioSelect)

    class Meta:
        model = Poll
        fields = ["choice"]


class AnswerForm(forms.ModelForm):
    ...
