from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response

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
        if self.action == "add_question":
            return QuestionSerializer
        return PollSerializer

    @action(detail=True, methods=['post'])
    def add_question(self, request, pk=None):
        poll = self.get_object()
        question_text = request.data.get('question_text')
        if question_text:
            question = Question.objects.create(poll=poll,
                                               question_text=question_text)
            return Response(QuestionSerializer(question).data, status=201)
        else:
            return Response({"error": "Question text is required."},
                            status=400)


class QuestionViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    queryset = Question.objects.select_related("poll")
    serializer_class = QuestionSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return QuestionDetailSerializer
        if self.action == "add_choice":
            return ChoiceSerializer
        return QuestionSerializer

    @action(detail=True, methods=['post'])
    def add_choice(self, request, pk=None):
        question = self.get_object()
        choice_text = request.data.get('choice_text')
        if choice_text:
            choice = Choice.objects.create(question=question,
                                           choice_text=choice_text)
            return Response(ChoiceSerializer(choice).data, status=201)
        else:
            return Response({"error": "Choice text is required."}, status=400)


class ChoiceViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
):
    queryset = Choice.objects.select_related("question__poll")
    serializer_class = ChoiceSerializer


class AnswerViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
):
    queryset = Answer.objects.none()
    serializer_class = AnswerSerializer

    def perform_create(self, serializer) -> None:
        serializer.save(owner=self.request.user)
