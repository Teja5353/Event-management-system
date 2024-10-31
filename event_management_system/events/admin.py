from django.contrib import admin
from .models import  Event, Attendee, Booking

admin.site.register(Event)
admin.site.register(Attendee)
admin.site.register(Booking)
# Register your models here.
