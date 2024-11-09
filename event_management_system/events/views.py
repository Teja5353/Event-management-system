from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event, Booking, Payment
from django.conf import settings
from .forms import EventForm, BookingForm, PaymentForm
from django.contrib.auth.forms import UserCreationForm
import stripe
from django.http import JsonResponse
from django.urls import reverse
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.views.decorators.csrf import csrf_exempt
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
        'upcoming_events': upcoming_events,
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
    return render(request, 'events/event_form.html', {'form': form})


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
    return render(request, 'events/booking_form.html', {'form': form, 'event': event})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/registration.html', {'form': form})


def payment(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    print(f"Creating payment session for event: {event.name}")  # Debugging statement

    # Create a Stripe checkout session
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': event.name,
                    },
                    'unit_amount': int(event.price * 100),
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('payment_success', args=[event.id])),
        cancel_url=request.build_absolute_uri(reverse('payment_cancel')),
    )
    print(f"Checkout session created: {checkout_session.id}")  # Debugging statement
    return JsonResponse({'id': checkout_session.id})



def payment_success(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Create a booking for the authenticated user
    attendee = request.user.attendee
    booking = Booking.objects.create(event=event, attendee=attendee)

    # Store the payment record
    Payment.objects.create(
        booking=booking,
        price=event.price,  # Use event price directly
        payment_status='completed',  # Mark payment as completed
        stripe_payment_id=request.GET.get('session_id')  # Get session ID from Stripe
    )

    # Render the success template and pass the event
    return render(request, 'events/success.html', {'event': event})



def payment_cancel(request):
    return render(request, 'events/payment_cancel.html')
def payment_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'events/payments.html', {
        'event': event,
        'stripe_public_key': settings.STRIPE_PUBLISHABLE_KEY,
    })
@login_required
def payment_list(request):
    payments = Payment.objects.filter(booking__attendee=request.user.attendee)
    return render(request, 'payments/payment_list.html', {'payments': payments})
