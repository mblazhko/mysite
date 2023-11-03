from rest_framework import viewsets, mixins


from polls.models import Poll, Question, Choice, Answer
from api.serializers import (
    AnswerSerializer,
    ChoiceSerializer,
    QuestionSerializer,
    QuestionDetailSerializer,
    PollSerializer,
    PollDetailSerializer,
    PollListSerializer,
)


class PollViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
):
    queryset = poll = Poll.objects.prefetch_related(
        "question_set__choice_set__answer_set"
    )
    serializer_class = PollSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return PollListSerializer
        if self.action == "retrieve":
            return PollDetailSerializer
        return PollSerializer


class QuestionViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
):
    queryset = Question.objects.select_related("choice_set")
    serializer_class = QuestionSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return QuestionDetailSerializer
        return QuestionSerializer


class ChoiceViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


class AnswerViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer