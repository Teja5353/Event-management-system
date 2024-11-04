from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event, Booking,Payment
from django.conf import settings
from .forms import EventForm, BookingForm, PaymentForm
from django.contrib.auth.forms import UserCreationForm
import stripe
import hashlib
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = settings.STRIPE_SECRET_KEY


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


@login_required
def initiate_payment(request, event_id):
    event = Event.objects.get(id=event_id)
    user = request.user
    amount = event.price  # Assuming each event has a price attribute

    # Generate the hash required by PayU
    hash_string = f"{settings.PAYU_MERCHANT_KEY}|{user.id}|{amount}|{event.name}|{user.first_name}|{user.email}|{settings.PAYU_SUCCESS_URL}|{settings.PAYU_FAILURE_URL}|{settings.PAYU_MERCHANT_SALT}"
    hash_object = hashlib.sha512(hash_string.encode())
    hash = hash_object.hexdigest()

    # Create a Payment object
    payment = Payment.objects.create(
        event=event,
        user=user,
        amount=amount,
        status="Pending"
    )

    # Data to be sent to PayU
    payu_data = {
        "key": settings.PAYU_MERCHANT_KEY,
        "txnid": str(payment.id),
        "amount": str(amount),
        "productinfo": event.name,
        "firstname": user.first_name,
        "email": user.email,
        "phone": user.profile.phone,  # Assuming user profile has a phone number
        "surl": settings.PAYU_SUCCESS_URL,
        "furl": settings.PAYU_FAILURE_URL,
        "hash": hash,
    }

    return render(request, "events/pay_with_payu.html", {"payu_data": payu_data, "payu_url": settings.PAYU_BASE_URL})
@csrf_exempt
def payment_success(request):
    txnid = request.POST.get('txnid')
    payment = Payment.objects.get(id=txnid)
    payment.status = "Success"
    payment.save()
    return HttpResponse("Payment successful")

@csrf_exempt
def payment_failure(request):
    txnid = request.POST.get('txnid')
    payment = Payment.objects.get(id=txnid)
    payment.status = "Failure"
    payment.save()
    return HttpResponse("Payment failed")