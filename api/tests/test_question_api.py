from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from api.serializers import QuestionDetailSerializer, ChoiceSerializer
from api.views import QuestionViewSet
from polls.models import Poll, Question, Choice


class QuestionApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="testpassword",
        )
        self.client.force_authenticate(self.user)
        self.question_viewset = QuestionViewSet()
        self.poll = Poll.objects.create(
                poll_name="poll_test",
                poll_description="description_test",
                owner=self.user,
            )
        self.question = Question.objects.create(
            poll=self.poll, question_text="question"
        )

    def tearDown(self) -> None:
        self.poll.delete()
        self.question.delete()


    def test_get_serializer_class_retrieve(self) -> None:
        self.question_viewset.action = "retrieve"
        serializer_class = self.question_viewset.get_serializer_class()
        self.assertEqual(serializer_class, QuestionDetailSerializer)

    def test_get_serializer_class_add_question(self) -> None:
        self.question_viewset.action = "add_choice"
        serializer_class = self.question_viewset.get_serializer_class()
        self.assertEqual(serializer_class, ChoiceSerializer)

    def test_add_choice_with_text(self) -> None:
        data = {"question": self.question.id, "choice_text": "choice"}

        url = f"/api/questions/{self.question.id}/add_choice/"
        res = self.client.post(url, data)

        choice = Choice.objects.get(id=res.data["id"])

        self.assertEqual(res.status_code, 201)
        self.assertIn(choice, self.question.choice_set.all())

    def test_add_choice_without_text(self) -> None:
        data = {"question": self.question.id, "choice_text": ""}

        url = f"/api/questions/{self.question.id}/add_choice/"
        res = self.client.post(url, data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.data["error"], "Choice text is required.")
