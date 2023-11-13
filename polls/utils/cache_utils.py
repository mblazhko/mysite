from django.core.cache import cache
from django.db import models
from django.db.models import QuerySet

from polls.models import Poll, Answer, Question
from .calculate_utils import calculate_charts_data


def get_popular_polls_cache() -> QuerySet:
    """Get the cache for popular polls and create if not cached."""
    popular_polls = cache.get("popular_polls")
    if not popular_polls:
        popular_polls = Poll.objects.annotate(
            num_answers=models.Count("question__choice__answer")
        ).order_by("-num_answers")[:10]
        cache.set("popular_polls", popular_polls)
    return popular_polls


def get_cached_poll(slug) -> Poll:
    """
    Get the poll from cache or database and cache it
    """
    poll = cache.get(f"poll_{slug}")
    if not poll:
        poll = Poll.objects.prefetch_related(
            "question_set__choice_set__answer_set"
        ).get(slug=slug)
        cache.set(f"poll_{slug}", poll)
    return poll


def get_cached_charts_data(poll) -> list:
    """
    Get cached charts data or calculate and cache it
    """
    charts_data = cache.get(f"charts_data_{poll.slug}")
    if not charts_data:
        questions = poll.question_set.all()
        charts_data = calculate_charts_data(questions)
        cache.set(f"charts_data_{poll.slug}", charts_data)
    return charts_data


def get_has_voted_cache(user, poll) -> bool:
    """Get the value has voted or not and cache it if not cached"""
    has_voted = cache.get(f"{user}_{poll.slug}_voted")
    if not has_voted:
        has_voted = Answer.objects.filter(
            owner=user,
            choice__question__poll=poll
        ).exists()
        cache.set(
            f"{user}_{poll.slug}_voted",
            has_voted
        )

    return has_voted


def get_poll_questions_cache(poll) -> list:
    questions = cache.get(f"{poll.slug}_questions")
    if not questions:
        questions = Question.objects.prefetch_related(
            "choice_set"
        ).filter(poll=poll)
        cache.set(f"{poll.slug}_questions", questions)
    return questions
