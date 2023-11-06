from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from polls.models import Poll, Question, Choice, Answer


class QuestionApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpassword",
        )
        self.client.force_authenticate(self.user)
        self.poll = (
            Poll.objects.create(
                poll_name="poll_test",
                poll_description="description_test",
                owner=self.user,
            ),
        )
        poll = Poll.objects.get(poll_name="poll_test")
        self.question = Question.objects.create(
            poll=poll, question_text="question"
        )
        question = Question.objects.get(question_text="question")
        self.choice = Choice.objects.create(
            question=question, choice_text="choice"
        )

    def test_perform_create_answer(self) -> None:
        data = {
            "choice": self.choice.id,
        }

        url = "/api/answers/"
        res = self.client.post(url, data)

        self.assertEqual(res.status_code, 201)

        answer = Answer.objects.get(id=res.data["id"])
        self.assertEqual(answer.owner.id, self.user.id)
