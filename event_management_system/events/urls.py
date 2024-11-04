from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('create/', views.event_create, name='event_create'),
    path('book/<int:event_id>/', views.book_event, name='book_event'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('register/', views.register, name='register'),  # Registration URL
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('initiate_payment/<int:event_id>/', views.initiate_payment, name="initiate_payment"),
    path('payment_success/', views.payment_success, name="payment_success"),
    path('payment_failure/', views.payment_failure, name="payment_failure"),
]
