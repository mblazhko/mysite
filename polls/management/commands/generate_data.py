from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
import random
from polls.models import Poll, Question, Choice, Answer


class Command(BaseCommand):
    help = "Generate random data and fill the database."

    def handle(self, *args, **kwargs):
        superuser = get_user_model().objects.create_superuser(
            email="admin@admin.com",
            password="V!5WucFeReMQ7fg",
            first_name="TestFirstName",
            last_name="TestLastName",
        )

        # generate 100 users
        for i in range(1, 1001):
            get_user_model().objects.create_user(
                email=f"user_{i}@user.com",
                password=f"V!5WucFeReMQ7fg{i}",
                first_name=f"FirstName{i}",
                last_name=f"LastName{i}",
            )

        # Generate 1000 Polls
        for i in range(1, 1001):
            poll = Poll.objects.create(
                poll_name=f"Poll {i}",
                poll_description=f"Description for Poll {i}",
                owner=superuser,
            )

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

        users = get_user_model().objects.all()
        questions = Question.objects.all()

        for user in users:
            for question in questions:
                random_choice = random.choice(question.choice_set.all())
                Answer.objects.create(owner=user, choice=random_choice)

        self.stdout.write(
            self.style.SUCCESS("Successfully generated random data.")
        )
