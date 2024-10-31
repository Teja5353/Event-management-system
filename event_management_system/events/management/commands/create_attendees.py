# events/management/commands/create_attendees.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from events.models import Attendee

class Command(BaseCommand):
    help = 'Create missing Attendee profiles for existing users'

    def handle(self, *args, **kwargs):
        users_without_profiles = User.objects.filter(attendee__isnull=True)
        for user in users_without_profiles:
            Attendee.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(f"Created Attendee for {user.username}"))
