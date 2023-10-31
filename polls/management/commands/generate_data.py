from django.core.management.base import BaseCommand
import random
from polls.models import Poll, Question, Choice, Answer


class Command(BaseCommand):
    help = 'Generate random data and fill the database.'

    def handle(self, *args, **kwargs):
        # Generate 1000 Polls
        for i in range(1000):
            poll = Poll.objects.create(poll_name=f'Poll {i + 1}',
                                       poll_description=f'Description for Poll {i + 1}')

            # Generate 4 Questions for each Poll
            for j in range(4):
                question = Question.objects.create(poll=poll,
                                                   question_text=f'Question {j + 1} for Poll {i + 1}')

                # Generate 5 Choices for each Question
                for k in range(5):
                    Choice.objects.create(question=question,
                                                   choice_text=f'Choice {k + 1} for Question {j + 1} in Poll {i + 1}')

        choices = Choice.objects.all()

        for _ in range(100000):
            random_choice = random.choice(choices)
            Answer.objects.create(choice=random_choice)

        self.stdout.write(
            self.style.SUCCESS('Successfully generated random data.'))
