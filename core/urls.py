# core/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),           # ← Startseite
    path('about/', views.about, name='about'),
    path('skills/', views.skills, name='skills'),
    path('contact/', views.contact, name='contact'),
    path('about-this-portfolio/', views.about_portfolio, name='about_portfolio'),
    path('in-progress/', views.in_progress, name='in_progress'),
]