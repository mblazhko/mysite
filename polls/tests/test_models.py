from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.text import slugify

from polls.models import Poll, Question, Answer, Choice


class ModelTest(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            email="test@test.com",
            password="test_123",
            first_name="TestFirstName",
            last_name="TestLastName",
        )
        self.poll = Poll.objects.create(
            poll_name="Test poll",
            poll_description="Test poll description",
            owner=user,
        )
        self.question = Question.objects.create(
            poll=self.poll,
            question_text="Test Question",
        )
        self.choice = Choice.objects.create(
            question=self.question, choice_text="Test Choice 1"
        )
        self.answer = Answer.objects.create(
            choice=self.choice,
            owner=user,
        )

    def test_poll_save(self) -> None:
        self.assertEqual(self.poll.slug, slugify(self.poll.poll_name))

    def test_poll_str(self) -> None:
        self.assertEqual(str(self.poll), self.poll.poll_name)

    def test_question_str(self) -> None:
        self.assertEqual(str(self.question), self.question.question_text)

    def test_choice_str(self) -> None:
        self.assertEqual(
            str(self.choice),
            f"{self.question.question_text} [{self.choice.choice_text}]",
        )

    def test_answer_str(self) -> None:
        self.assertEqual(
            str(self.answer),
            f"{self.choice.choice_text} [{self.choice.question.question_text}]",
        )
