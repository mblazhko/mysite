from django.core.cache import cache
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from polls.models import Answer, Question


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
