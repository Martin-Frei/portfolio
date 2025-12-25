from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    # path('get-guest-modal/', views.get_guest_modal, name='get_guest_modal'),
    # path('guest-login/', views.guest_login_attempt, name='guest_login_attempt'),
]