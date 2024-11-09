from django.contrib import admin
from .models import  Event, Attendee, Booking , Payment

admin.site.register(Event)
admin.site.register(Attendee)
admin.site.register(Booking)
# Register your models here.
admin.site.register(Payment)