import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from polls.models import Answer, Choice, Poll, Question


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

        # generate 20 users
        for i in range(1, 21):
            get_user_model().objects.create_user(
                email=f"user_{i}@user.com",
                password=f"V!5WucFeReMQ7fg{i}",
                first_name=f"FirstName{i}",
                last_name=f"LastName{i}",
            )

        self.stdout.write("20 users created")

        # Generate 1000 Polls
        for i in range(1, 1001):
            poll = Poll.objects.create(
                poll_name=f"Poll {i}",
                poll_description=f"Description for Poll {i}",
                owner=superuser,
            )

            self.stdout.write(f"Poll {poll.poll_name} created")

            # Generate 4 Questions for each Poll
            for j in range(1, 5):
                question = Question.objects.create(
                    poll=poll, question_text=f"Question {j} for Poll {i}"
                )

                # Generate 5 Choices for each Question
                for k in range(1, 6):
                    Choice.objects.create(
                        question=question,
                        choice_text=f"Choice {k} for Question {j} in Poll {i}",
                    )

            self.stdout.write(
                f"Questions and Choices for {poll.poll_name} created"
            )

        users = get_user_model().objects.all()
        questions = Question.objects.all()

        for user in users:
            for question in questions:
                random_choice = random.choice(question.choice_set.all())
                Answer.objects.create(owner=user, choice=random_choice)

            self.stdout.write(f"User {user.email} voted")

        self.stdout.write(
            self.style.SUCCESS("Successfully generated random data.")
        )
