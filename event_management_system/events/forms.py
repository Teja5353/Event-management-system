from django import forms
from .models import Event, Booking

from django.forms import TextInput, DateInput, TimeInput,SelectDateWidget


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'location', 'date', 'time'];
        widgets = {
            'name': TextInput(
                attrs={
                    'class': "form-control-name",
                    'placeholder': "Enter Event Name",
                    'size': '30px',
                }
            ),
            'description': TextInput(
                attrs={
                    'class': "form-control-description",
                    'placeholder': "About Event",
                    'size' : '20px',
                }
            ),
            'location': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': "Enter your Event's Location"
                }
            ),
            'date': SelectDateWidget(
                attrs={
                    'class': 'form-control-date',
                    'type': 'date',
                }
            ),
            'time': TimeInput(
                attrs={
                    'class': 'form-control-time',
                    'type' : "time"
                }
            )
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['event']
class PaymentForm(forms.Form):
    event_id = forms.IntegerField(widget=forms.HiddenInput())