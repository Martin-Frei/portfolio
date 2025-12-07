from django.urls import path
from . import views

app_name = 'rps'

urlpatterns = [
    path('', views.main, name='game'),
    path('game/', views.game, name='game'),
    path('reset/', views.resetGame, name='reset'),
]