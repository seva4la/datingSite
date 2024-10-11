from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics
from dating.models import User
from dating.serializers import *

def dating(request):
    return HttpResponse("<h1>Сайт знакомств<h1>")


class UserApiListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

class UserApiUpdateDescription(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateDescriptionSerializer
    #serializer_class =  UserListSerializer

class UserApiDelete(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

class UserApiRetriveView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer

class UserApiCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserListSerializer