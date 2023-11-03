from rest_framework import serializers
from polls.models import Poll, Question, Choice, Answer


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("id", "choice", "owner")


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ("id", "question", "choice_text")


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("id", "poll", "question_text")


class QuestionDetailSerializer(QuestionSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ("id", "question_text", "choices")


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = (
            "id",
            "poll_name",
            "poll_description",
            "pub_date",
            "slug"
        )


class PollDetailSerializer(PollSerializer):
    questions = QuestionDetailSerializer(many=True)

    class Meta:
        model = Poll
        fields = (
            "id",
            "poll_name",
            "poll_description",
            "questions",
            "pub_date",
            "slug"
        )


class PollListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ("id", "poll_name", "poll_description")
