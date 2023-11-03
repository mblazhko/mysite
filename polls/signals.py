from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save, pre_delete, post_delete
from django.dispatch import receiver

from polls.models import Answer, Question, Poll


@receiver(signal=pre_delete, sender=Question)
@receiver(signal=pre_delete, sender=Answer)
@receiver(signal=post_save, sender=Question)
@receiver(signal=post_save, sender=Answer)
def invalidate_poll_cache(**kwargs) -> None:
    print("Invalidating poll cache")
    instance = kwargs['instance']
    if isinstance(instance, Answer):
        cache_key = f"poll_{instance.choice.question.poll.slug}"
    if isinstance(instance, Question):
        cache_key = f"poll_{instance.poll.slug}"
    cache.delete(cache_key)


@receiver(signal=post_delete, sender=Poll)
@receiver(signal=post_save, sender=Answer)
def invalidate_popular_poll_cache(**kwargs) -> None:
    popular_polls_before = cache.get("popular_polls")
    popular_polls_after = Poll.objects.annotate(
        num_answers=models.Count("question__choice__answer")
    ).order_by("-num_answers")[:10]

    if popular_polls_before != popular_polls_after:
        cache.delete("popular_polls")
        cache.set("popular_polls", popular_polls_after)
