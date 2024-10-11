from django.urls import path
from . import views

urlpatterns = [
    path('', views.dating, name='MainPage')
]