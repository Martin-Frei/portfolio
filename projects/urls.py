# projects/urls.py
from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('', views.public_list, name='public_list'),                    # /projects/
    path('secret-lab/', views.secret_lab, name='secret_lab'),           # /projects/secret-lab/
    path('<int:pk>/', views.project_detail, name='project_detail'),     # ← DIESE ZEILE HINZUFÜGEN!
]