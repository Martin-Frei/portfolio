"""
Icon-Challenge URLs
"""

from django.urls import path
from . import views

app_name = 'icon_challenge'

urlpatterns = [
    path('start/<str:context_type>/', views.start_challenge, name='start'),
    path('verify/<str:context_type>/', views.verify_challenge_attempt, name='verify'),
    path('signup-prepare/', views.signup_prepare, name='signup_prepare'),
    path('contact-prepare/', views.contact_prepare, name='contact_prepare'),
]