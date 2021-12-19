from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=get_user_model())
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, username=instance.username, password=instance.password, email=instance.email,
                               first_name=instance.first_name, last_name=instance.last_name, date_joined=instance.date_joined)
    else:
        instance.profile.save()
