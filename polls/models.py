from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Poll(models.Model):
    poll_name = models.CharField(max_length=200)
    poll_description = models.TextField(max_length=1000)
    pub_date = models.DateTimeField("date published", default=timezone.now)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self) -> str:
        return self.poll_name

    @property
    def publication_date(self) -> str:
        date = self.pub_date.strftime("%d-%m-%Y")
        return f"Published at: {date}"

    def save(self, *args, **kwargs) -> None:
        """Generate slug during creation the poll"""
        if not self.slug:
            self.slug = slugify(self.poll_name)
        super().save(*args, **kwargs)


class Question(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.question.question_text} [{self.choice_text}]"


class Answer(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return (
            f"{self.choice.choice_text} [{self.choice.question.question_text}]"
        )
