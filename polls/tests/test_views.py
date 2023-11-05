from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from polls.models import Poll, Question, Answer, Choice


class BaseTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="test_123",
            first_name="TestFirstName",
            last_name="TestLastName"
        )
        self.client.force_login(self.user)
        self.poll = Poll.objects.create(
            poll_name="Test poll",
            poll_description="Test poll description",
            owner=self.user
        )
        self.question = Question.objects.create(
            poll=self.poll,
            question_text="Test Question",
        )
        self.choice_1 = Choice.objects.create(
            question=self.question,
            choice_text="Test Choice 1"
        )
        self.choice_2 = Choice.objects.create(
            question=self.question,
            choice_text="Test Choice 2"
        )
        self.answer = Answer.objects.create(
            choice=self.choice_1,
            owner=self.user,
        )


class PrivatePollTest(BaseTest):
    def test_retrieve_poll_detail(self) -> None:
        poll_detail_url = reverse(
            "polls:poll-detail",
            kwargs={"slug": self.poll.slug}
        )
        response = self.client.get(poll_detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['poll'], self.poll)
        self.assertTemplateUsed(response, 'polls/poll_detail.html')

    def test_create_poll(self) -> None:
        poll_create_url = reverse("polls:poll-create")
        response = self.client.post(poll_create_url, {
            'title': 'Test Poll Title',
            'description': 'Test Poll Description',
            'questions': ['Question 1', 'Question 2'],
            'options_Question 1': ['Option 1', 'Option 2'],
            'options_Question 2': ['Option A', 'Option B'],
        })

        poll = Poll.objects.get(poll_name="Test Poll Title")

        self.assertEqual(Poll.objects.count(), 2)
        self.assertEqual(Question.objects.count(), 3)
        self.assertEqual(Choice.objects.count(), 6)

        self.assertRedirects(
            response,
            reverse('polls:poll-detail', kwargs={"slug": poll.slug})
        )

    def test_poll_delete(self) -> None:
        response = self.client.post(
            reverse(
                'polls:poll-delete',
                kwargs={"slug": self.poll.slug}
            )
        )

        polls = Poll.objects.all()

        self.assertEqual(response.status_code, 302)
        self.assertNotIn(self.poll, polls)


class PublicPollTest(BaseTest):
    def test_detail_poll_login_required(self) -> None:
        self.client.logout()
        response = self.client.get(reverse(
            "polls:poll-detail",
            kwargs={"slug": self.poll.slug})
        )

        self.assertEquals(response.status_code, 302)

    def test_retrieve_poll_list(self) -> None:
        index_url = reverse("polls:index")
        response = self.client.get(index_url)
        polls = Poll.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["poll_list"]), list(polls))
        self.assertTemplateUsed(response, "polls/index.html")

    def test_retrieve_poll_results(self) -> None:
        poll_results_url = reverse(
            "polls:poll-results",
            kwargs={"slug": self.poll.slug}
        )
        response = self.client.get(poll_results_url)

        data = [{
            "id": self.question.id,
            "labels": [
                choice.choice_text for choice in self.question.choice_set.all()
            ],
            "data": [
                choice.answer_set.count()
                for choice in self.question.choice_set.all()
            ],
        }]

        self.assertEqual(response.context["charts_data"], data)
        self.assertEqual(response.context["poll"], self.poll)
        self.assertTemplateUsed(response, "polls/results.html")



























