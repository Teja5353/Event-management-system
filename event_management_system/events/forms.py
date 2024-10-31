from django import forms
from .models import Event, Booking


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['organizer']

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['event']
