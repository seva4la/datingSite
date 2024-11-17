from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics
from dating.models import User
from dating.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


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

class UserLikeAPIView(APIView):

    permission_classes = [IsAuthenticated] #проверяем аутентифицирован ли пользователь

    def post(self, request, *args, **kwargs):
        user = request.user                 # 'user' это пользователь, который дал пост запрос
        liked_user_id = request.data.get('liked_user_id') # поле, в которое вводится id пользователя, которого лайкнут

        try:
            liked_user = User.objects.get(id=liked_user_id)
            if user.like_user(liked_user):
                return Response({'message': 'Пользователь лайкнут.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Нельзя лайкнуть пользователя дважды или самого себя.'},
                                status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'message': 'Пользователь не найден.'}, status=status.HTTP_404_NOT_FOUND)


class UserLikedMeAPIView(APIView):
    """
    API для получения списка пользователей, которые лайкнули текущего пользователя.
    """
    permission_classes = [IsAuthenticated]  # Только аутентифицированные пользователи

    def get(self, request, *args, **kwargs):
        # Текущий пользователь
        current_user = request.user

        # Пользователи, которые лайкнули текущего пользователя
        liked_by_users = User.objects.filter(likes=current_user)

        # Сериализация данных
        serializer = UserListSerializer(liked_by_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)