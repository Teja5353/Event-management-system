from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('events/', include('events.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    # Redirect the root URL to the event list page
    path('', lambda request: redirect('event_list')),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
]
