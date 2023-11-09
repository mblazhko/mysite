from typing import Type

from django.db.models.sql import Query
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, Serializer
from polls.models import Poll, Question, Choice, Answer
from api.serializers import (
    ChoiceSerializer,
    QuestionSerializer,
    QuestionDetailSerializer,
    PollSerializer,
    PollDetailSerializer,
    PollListSerializer,
    VoteSerializer,
)


class PollViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = poll = Poll.objects.prefetch_related(
        "question_set__choice_set__answer_set"
    )
    serializer_class = PollSerializer

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == "list":
            return PollListSerializer
        if self.action == "retrieve":
            return PollDetailSerializer
        if self.action == "add_question":
            return QuestionSerializer
        if self.action == "vote":
            return VoteSerializer
        return PollSerializer

    def get_queryset(self) -> Query:
        """Show only user's created poll"""
        queryset = self.queryset

        return queryset.filter(owner=self.request.user)

    def perform_create(self, serializer) -> None:
        """Auto-assign user to the created poll"""
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["post"])
    def add_question(self, request, pk=None) -> Response:
        """Action to add a question to the chosen poll"""
        poll = self.get_object()
        if not self.request.user.is_staff:
            if poll.owner != self.request.user:
                return Response(
                    {
                        "error": "You do not have permission "
                        "to add a question to this poll."
                    },
                    status=403,
                )

        question_text = request.data.get("question_text")
        if question_text:
            question = Question.objects.create(
                poll=poll, question_text=question_text
            )
            return Response(
                QuestionSerializer(question).data,
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"error": "Question text is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @action(detail=True, methods=["post"])
    def vote(self, request, pk=None) -> Response:
        """
        Action to vote a current poll.
        User have to enter choice id to all poll's questions.
        Every choice id must be unique.
        Every choice must belong to a different question.
        Every question must belong to the same poll.
        """
        poll = self.get_object()
        user = request.user

        serializer = VoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        answers = serializer.validated_data.get("answers", [])
        questions_count = poll.question_set.count()
        if len(answers) != questions_count:
            return Response(
                {
                    "error": f"You must provide answers "
                    f"for all {questions_count} questions"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(set(answers)) != len(answers):
            return Response(
                {"error": f"Every choice must be unique"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        unique_choices = set()
        for choice_id in answers:
            choice = Choice.objects.get(id=choice_id)
            if choice.question.id in unique_choices:
                return Response(
                    {
                        "error": "Each choice must belong to "
                        "a different question."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            unique_choices.add(choice.question.id)

        questions = Question.objects.filter(id__in=unique_choices)
        if questions.filter(poll=poll).count() != len(answers):
            return Response(
                {"error": "All questions must belong to the same poll."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        for choice_id in answers:
            choice = Choice.objects.get(id=choice_id)
            existing_answer = Answer.objects.filter(
                choice__question=choice.question, owner=user
            ).first()
            if existing_answer:
                existing_answer.choice = choice
                existing_answer.save()
            else:
                Answer.objects.create(owner=user, choice=choice)

        return Response(
            {"message": "Votes submitted successfully."},
            status=status.HTTP_200_OK,
        )


class QuestionViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = Question.objects.select_related("poll")
    serializer_class = QuestionSerializer

    def get_serializer_class(self) -> Type[ModelSerializer]:
        if self.action == "retrieve":
            return QuestionDetailSerializer
        if self.action == "add_choice":
            return ChoiceSerializer
        return QuestionSerializer

    def get_queryset(self) -> Query:
        """Show questions created by this user"""
        queryset = self.queryset

        return queryset.filter(poll__owner=self.request.user)

    @action(detail=True, methods=["post"])
    def add_choice(self, request, pk=None) -> Response:
        """Add a choice to the chosen question"""
        question = self.get_object()
        if not self.request.user.is_staff:
            if question.poll.owner != self.request.user:
                return Response(
                    {
                        "error": "You do not have permission to add a choice to "
                        "this question."
                    },
                    status=403,
                )
        choice_text = request.data.get("choice_text")
        if choice_text:
            choice = Choice.objects.create(
                question=question, choice_text=choice_text
            )
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
        """Auto-assign current user to answer"""
        serializer.save(owner=self.request.user)
