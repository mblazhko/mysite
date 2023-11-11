from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_delete, post_save, pre_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from polls.models import Answer, Poll, Question, Choice


@receiver(signal=post_delete, sender=Poll)
@receiver(signal=pre_delete, sender=Question)
@receiver(signal=pre_delete, sender=Answer)
@receiver(signal=post_save, sender=Question)
@receiver(signal=post_save, sender=Answer)
def invalidate_poll_cache(sender, **kwargs) -> None:
    """
    Delete the poll results cache before deleting or after creating a
    Question or an Answer related with that poll
    """
    cache_key = ""
    instance = kwargs["instance"]
    if isinstance(instance, Poll):
        cache_key = f"poll_{instance.slug}"
    elif isinstance(instance, Answer):
        cache_key = f"poll_{instance.choice.question.poll.slug}"
    elif isinstance(instance, Question):
        cache_key = f"poll_{instance.poll.slug}"
    cache.delete(cache_key)


@receiver(signal=post_delete, sender=Poll)
@receiver(signal=post_save, sender=Answer)
def invalidate_popular_poll_cache(sender, **kwargs) -> None:
    """
    Delete the popular poll cache after creating
    or deleting an answer relating with the poll
    """
    popular_polls_before = cache.get("popular_polls")
    popular_polls_after = Poll.objects.annotate(
        num_answers=models.Count("question__choice__answer")
    ).order_by("-num_answers")[:10]

    if popular_polls_before != popular_polls_after:
        cache.delete("popular_polls")
        cache.set("popular_polls", popular_polls_after)


@receiver(signal=post_delete, sender=Poll)
@receiver(signal=post_delete, sender=Question)
@receiver(signal=post_delete, sender=Choice)
@receiver(signal=post_delete, sender=settings.AUTH_USER_MODEL)
@receiver(signal=post_save, sender=Question)
@receiver(signal=post_save, sender=Answer)
@receiver(signal=post_save, sender=Choice)
def invalidate_has_voted_cache(sender, **kwargs) -> None:
    """
    Invalidate the has_voted_cache after made changes with instance
    """
    instance = kwargs["instance"]
    user = None
    slug = None

    if isinstance(instance, Poll):
        user = instance.owner
        slug = instance.slug
    elif isinstance(instance, Question):
        user = instance.poll.owner
        slug = instance.poll.slug
    elif isinstance(instance, Choice):
        user = instance.question.poll.owner
        slug = instance.question.poll
    elif isinstance(instance, Answer):
        user = instance.owner
        slug = instance.choice.question.poll
    elif isinstance(instance, settings.AUTH_USER_MODEL):
        for poll in instance.poll_set.all():
            cache.delete(f"{instance}_{poll.slug}_voted")

    key = cache.get(f"{user}_{slug}_voted")
    cache.delete(key)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance, created, **kwargs) -> None:
    """Generate a new token after user creation"""
    if created:
        Token.objects.create(user=instance)
