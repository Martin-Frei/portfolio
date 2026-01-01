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
     # ========== CURRENT PROJECT (NEU!) ==========
    path('current-project/', views.current_project, name='current_project'),
    path('current-project/updates/', views.update_list_htmx, name='update_list_htmx'),
    path('current-project/update/<int:pk>/', views.update_detail_htmx, name='update_detail_htmx'),
    
]