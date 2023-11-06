from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import random
from polls.models import Poll, Question, Choice, Answer


class Command(BaseCommand):
    help = "Generate random data and fill the database."

    def handle(self, *args, **kwargs) -> None:

        self.stdout.write("Start generating random data")

        superuser = get_user_model().objects.create_superuser(
            email="admin@admin.com",
            password="V!5WucFeReMQ7fg",
            first_name="TestFirstName",
            last_name="TestLastName",
        )

        self.stdout.write(f"Superuser {superuser.email} created")
