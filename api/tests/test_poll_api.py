from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from api.serializers import (
    PollDetailSerializer,
    PollListSerializer,
    PollSerializer,
    QuestionSerializer
)
from api.views import PollViewSet
from polls.models import Choice, Poll, Question


class BasePollApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpassword",
        )
        self.client.force_authenticate(self.user)
        self.poll_viewset = PollViewSet()
        self.poll = Poll.objects.create(
            poll_name="poll_test",
            poll_description="description_test",
            owner=self.user,
        )
        self.question1 = Question.objects.create(
            question_text="Question 1",
            poll=self.poll
        )
        self.question2 = Question.objects.create(
            question_text="Question 2",
            poll=self.poll
        )
        self.choice1 = Choice.objects.create(
            choice_text="Choice 1", question=self.question1
        )
        self.choice2 = Choice.objects.create(
            choice_text="Choice 2", question=self.question1
        )
        self.choice3 = Choice.objects.create(
            choice_text="Choice 3", question=self.question2
        )
        self.vote_url = f"/api/polls/{self.poll.id}/vote/"

    def tearDown(self) -> None:
        self.poll.delete()
        self.question1.delete()
        self.question2.delete()
        self.choice1.delete()
        self.choice2.delete()
        self.choice3.delete()


class PollApiTest(BasePollApiTest):
    def test_vote_with_one_choice(self) -> None:
        data = {"answers": [self.choice1.id]}
        res = self.client.post(self.vote_url, data)

        self.assertEqual(res.status_code, 400)

    def test_vote_non_unique_choices(self) -> None:
        data = {"answers": [self.choice1.id, self.choice1.id]}
        res = self.client.post(self.vote_url, data)

        self.assertEqual(res.status_code, 400)

    def test_vote_with_choices_from_one_question(self) -> None:
        data = {"answers": [self.choice1.id, self.choice2.id]}
        res = self.client.post(self.vote_url, data)
        print(res.data)
        self.assertEqual(res.status_code, 400)

    def test_vote_with_valid_data(self) -> None:
        data = {"answers": [self.choice1.id, self.choice3.id]}
        res = self.client.post(self.vote_url, data)

        self.assertEqual(res.status_code, 201)

    def test_get_serializer_class_list(self) -> None:
        self.poll_viewset.action = "list"
        serializer_class = self.poll_viewset.get_serializer_class()
        self.assertEqual(serializer_class, PollListSerializer)

    def test_get_serializer_class_retrieve(self) -> None:
        self.poll_viewset.action = "retrieve"
        serializer_class = self.poll_viewset.get_serializer_class()
        self.assertEqual(serializer_class, PollDetailSerializer)

    def test_get_serializer_class_add_question(self) -> None:
        self.poll_viewset.action = "add_question"
        serializer_class = self.poll_viewset.get_serializer_class()
        self.assertEqual(serializer_class, QuestionSerializer)

    def test_get_serializer_class_default(self) -> None:
        self.poll_viewset.action = "other_action"
        serializer_class = self.poll_viewset.get_serializer_class()
        self.assertEqual(serializer_class, PollSerializer)

    def test_perform_create(self) -> None:
        data = {
            "poll_name": "poll",
            "poll_description": "description",
        }

        url = "/api/polls/"
        res = self.client.post(url, data)

        self.assertEqual(res.status_code, 201)
        poll = Poll.objects.get(id=res.data["id"])
        self.assertEqual(poll.owner.id, self.user.id)

    def test_add_question_with_text(self) -> None:
        data = {"poll": self.poll.id, "question_text": "question"}
        url = f"/api/polls/{self.poll.id}/add_question/"
        res = self.client.post(url, data)

        question = Question.objects.get(id=res.data["id"])
        poll_questions = Question.objects.filter(poll=self.poll)

        self.assertEqual(res.status_code, 201)

        self.assertIn(question, poll_questions)

    def test_add_question_without_text(self) -> None:
        data = {"poll": self.poll.id, "question_text": ""}
        url = f"/api/polls/{self.poll.id}/add_question/"
        res = self.client.post(url, data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data["error"], "Question text is required.")
