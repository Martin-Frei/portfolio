from django.urls import path
from . import views

app_name = 'bmi'  # ==> {% url 'bmi:calculator' %}

urlpatterns = [
    path('', views.calculator, name='calculator'),  # /bmi/
    path('get_input/', views.get_input, name='get_input'),  # /bmi/get_input/
]