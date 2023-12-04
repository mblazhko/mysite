import random
from concurrent.futures import ThreadPoolExecutor

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

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

        # Generate 20 users concurrently
        users = self.generate_users_concurrently()
        self.stdout.write("20 users created")

        # Generate 1000 Polls concurrently
        polls = self.generate_poll_concurrently(user=superuser)
        self.stdout.write("1000 polls created")

        # Generate Questions and Choices concurrently
        questions = self.generate_question_concurrently(polls=polls)
        self.stdout.write("Questions and Choices created")

        # Vote creation concurrently
        self.generate_votes_concurrently(users=users, questions=questions)

        self.stdout.write(
            self.style.SUCCESS("Successfully generated random data.")
        )

    def generate_users_concurrently(self) -> list:
        with ThreadPoolExecutor() as executor:
            users_data = [
                {
                    "email": f"user_{i}@user.com",
                    "password": f"V!5WucFeReMQ7fg{i}",
                    "first_name": f"FirstName{i}",
                    "last_name": f"LastName{i}",
                }
                for i in range(1, 21)
            ]

            return list(executor.map(self.create_user, users_data))

    @staticmethod
    def create_user(user_data: dict):
        return get_user_model().objects.create_user(
            email=user_data["email"],
            password=user_data["password"],
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
        )

    def generate_poll_concurrently(self, user) -> list[Poll]:
        with ThreadPoolExecutor() as executor:
            polls_data = [
                {
                    "poll_name": f"Poll {i}",
                    "poll_description": f"Description for Poll {i}",
                    "owner": user,
                }
                for i in range(1, 1001)
            ]

            return list(executor.map(self.create_poll, polls_data))

    @staticmethod
    def create_poll(poll_data: dict) -> Poll:
        return Poll.objects.create(
            poll_name=poll_data["poll_name"],
            poll_description=poll_data["poll_description"],
            owner=poll_data["owner"],
        )

    def generate_question_concurrently(
        self, polls: list[Poll]
    ) -> list[Question]:
        with ThreadPoolExecutor() as executor:
            questions_choices_data = [
                {
                    "poll": poll,
                    "question_text": f"Question {j} for Poll {poll.poll_name}",
                }
                for poll in polls
                for j in range(1, 6)
            ]

            return list(
                executor.map(self.create_question, questions_choices_data)
            )

    def create_question(self, question_data: dict) -> Question:
        poll = question_data["poll"]
        question_text = question_data["question_text"]

        question = Question.objects.create(
            poll=poll, question_text=question_text
        )

        # Generate 5 Choices for each Question
        self.create_choices_for_question(question, poll)

        return question

    @staticmethod
    def create_choices_for_question(question: Question, poll: Poll) -> None:
        for k in range(1, 6):
            Choice.objects.create(
                question=question,
                choice_text=f"Choice {k} for {question} in {poll.poll_name}",
            )

    def generate_votes_concurrently(
        self, users: list, questions: list[Question]
    ) -> None:
        with ThreadPoolExecutor() as executor:
            votes_data = [
                {"user": user, "questions": questions} for user in users
            ]
            list(executor.map(self.create_votes, votes_data))

    @transaction.atomic
    def create_votes(self, votes_data: dict) -> None:
        user = votes_data["user"]
        questions = votes_data["questions"]
        answers = []
        for question in questions:
            random_choice = random.choice(question.choice_set.all())
            answers.append(Answer(owner=user, choice=random_choice))

        Answer.objects.bulk_create(answers)

        self.stdout.write(f"User {user.email} voted")
