from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics
from dating.models import User
from dating.serializers import *

def dating(request):
    return HttpResponse("<h1>Сайт знакомств<h1>")

class UserApiRegistrate(generics.CreateAPIView): #регистрация
    queryset = User.objects.all()
    serializer_class = UserRegistrateSerializer

class UserUpdate(generics.UpdateAPIView): # обновление
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer

class UserApiListView(generics.ListAPIView): #все пользователи
    queryset = User.objects.all()
    serializer_class = UserListSerializer

class UserApiRetriveView(generics.RetrieveAPIView): # конкретный пользователь
    queryset = User.objects.all()
    serializer_class = UserListSerializer

class UserApiDelete(generics.DestroyAPIView): # удаление пользователя
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    lookup_field = 'pk'  # Используем UUID


