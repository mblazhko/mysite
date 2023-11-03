from django.utils import timezone
from rest_framework import serializers
from polls.models import Poll, Question, Choice, Answer


class AnswerSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(read_only=True)
    choice = serializers.PrimaryKeyRelatedField(queryset=Choice.objects.select_related("question__poll"))

    class Meta:
        model = Answer
        fields = ("id", "choice", "owner")


class ChoiceSerializer(serializers.ModelSerializer):
    question = serializers.CharField(read_only=True, source="question__question_text")

    class Meta:
        model = Choice
        fields = ("id", "question", "choice_text")


class QuestionSerializer(serializers.ModelSerializer):
    poll = serializers.CharField(read_only=True, source="poll__poll_name")

    class Meta:
        model = Question
        fields = ("id", "poll", "question_text")


class QuestionDetailSerializer(QuestionSerializer):
    choices = ChoiceSerializer(many=True, source="choice_set")

    class Meta:
        model = Question
        fields = ("id", "question_text", "choices")


class PollSerializer(serializers.ModelSerializer):
    slug = serializers.CharField(read_only=True)
    pub_date = serializers.DateTimeField(default=timezone.now(), read_only=True)

    class Meta:
        model = Poll
        fields = (
            "id",
            "poll_name",
            "poll_description",
            "pub_date",
            "slug"
        )

    def create(self, validated_data):
        validated_data['pub_date'] = timezone.now()
        return super(PollSerializer, self).create(validated_data)


class PollDetailSerializer(PollSerializer):
    questions = QuestionDetailSerializer(many=True, source="question_set")

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
