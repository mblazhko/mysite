from typing import Callable

from django.utils import timezone
from rest_framework import serializers

from polls.models import Choice, Poll, Question


class ChoiceSerializer(serializers.ModelSerializer):
    """Serializer for Choice objects with an auto-assigned question"""

    question = serializers.CharField(
        read_only=True, source="question__question_text"
    )

    class Meta:
        model = Choice
        fields = ("id", "question", "choice_text")


class ChoiceDeleteSerializer(serializers.Serializer):
    choice_id = serializers.IntegerField()


class QuestionSerializer(serializers.ModelSerializer):
    """Default serializer for Question objects with an auto-assigned poll"""

    poll = serializers.CharField(read_only=True, source="poll__poll_name")

    class Meta:
        model = Question
        fields = ("id", "poll", "question_text")


class QuestionDetailSerializer(QuestionSerializer):
    """
    Detail Question object serializer with displaying information about
    assigned choices
    """

    choices = ChoiceSerializer(many=True, source="choice_set")

    class Meta:
        model = Question
        fields = ("id", "question_text", "choices")


class PollSerializer(serializers.ModelSerializer):
    """
    Default Poll object serializer with auto-generated publication date,
    slug and auto-assigned current user
    """

    slug = serializers.CharField(read_only=True)
    pub_date = serializers.DateTimeField(
        default=timezone.now(), read_only=True
    )
    owner = serializers.CharField(read_only=True)

    class Meta:
        model = Poll
        fields = (
            "id",
            "poll_name",
            "poll_description",
            "pub_date",
            "slug",
            "owner",
        )

    def create(self, validated_data) -> Callable:
        """Auto generate a publication date"""
        validated_data["pub_date"] = timezone.now()
        return super(PollSerializer, self).create(validated_data)


class PollDetailSerializer(PollSerializer):
    """Serializer for Poll detail view"""

    questions = QuestionDetailSerializer(many=True, source="question_set")

    class Meta:
        model = Poll
        fields = (
            "id",
            "poll_name",
            "poll_description",
            "questions",
            "pub_date",
            "slug",
        )


class PollListSerializer(serializers.ModelSerializer):
    """Serializer for list view for Poll objects"""

    class Meta:
        model = Poll
        fields = ("id", "poll_name", "poll_description")


class VoteSerializer(serializers.Serializer):
    answers = serializers.ListField(child=serializers.IntegerField())
