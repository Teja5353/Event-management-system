from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Attendee


@receiver(user_logged_in)
def create_attendee_on_login(sender, request, user, **kwargs):
    # Check if an Attendee instance already exists for this user
    Attendee.objects.get_or_create(user=user)