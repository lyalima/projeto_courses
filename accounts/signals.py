from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from utils.send_verification_email import send_verification_email


@receiver(post_save, sender=CustomUser)
def send_verification_code(sender, instance, created, **kwargs):
    if created:
        send_verification_email(instance)