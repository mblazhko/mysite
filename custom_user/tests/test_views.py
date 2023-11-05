from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from polls.models import Poll


PROFILE_URL = reverse("custom_user:user_profile")
UPDATE_PROFILE_URL = reverse("custom_user:update_profile")


class UserTest(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = get_user_model().objects.create_superuser(
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

    def test_user_profile(self) -> None:
        response = self.client.get(PROFILE_URL)
        polls = Poll.objects.filter(owner=self.user)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], self.user)
        self.assertEqual(list(response.context['polls']), list(polls))

    def test_update_user_profile(self) -> None:
        response = self.client.post(UPDATE_PROFILE_URL, {
            "first_name": "FirstName",
            "last_name": "LastName"
        })

        updated_user = get_user_model().objects.get(id=self.user.id)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(updated_user.first_name, "FirstName")
        self.assertEqual(updated_user.last_name, "LastName")
