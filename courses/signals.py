from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Course, Vacancie


@receiver([post_save, post_delete], sender=Course)
@receiver([post_save, post_delete], sender=Vacancie)
def clear_cache(sender, **kwargs):
    cache.clear()
