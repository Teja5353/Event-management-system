from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event,Booking
from .forms import EventForm, BookingForm
from django.contrib.auth.forms import UserCreationForm

def event_list(request):
    user = request.user
    if user.is_authenticated:
        booked_events = Event.objects.filter(booking__attendee=user.attendee)
        upcoming_events = Event.objects.exclude(id__in=booked_events)
    else:
        booked_events = None
        upcoming_events = Event.objects.all()
    return render(request, 'events/event_list.html', {
        'booked_events': booked_events,
        'upcoming_events':upcoming_events,
    })

@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/event_form.html', {'form':form})

@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.attendee = request.user.attendee
            booking.save()
            return redirect('event_list')
    else:
        form = BookingForm(initial={'event': event})
    return render(request, 'events/booking_form.html', {'form':form, 'event':event})
def register(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request,'registration/registration.html',{'form':form})

# Create your views here.
