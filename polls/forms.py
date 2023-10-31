from django import forms

from polls.models import Answer


class AnswerForm(forms.ModelForm):
    choice = forms.ChoiceField(widget=forms.RadioSelect)
    class Meta:
        model = Answer
        fields = ['choice']
