from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django import forms
class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Attendee(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} 's Attendee Profile"


class Booking(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.attendee.user.username} booked {self.event.name} on {self.booking_date}"
class Payment(models.Model):
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ])
    stripe_payment_id = models.CharField(max_length=100, null=True, blank=True)  # Optional: store Stripe payment ID

    def __str__(self):
        return f"Payment of {self.price} for booking {self.booking.id} - Status: {self.payment_status}"
# Create your models here.

