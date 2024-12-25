from rest_framework import serializers
import os
from dating.models import User, validate_age
from django.db import models
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated


class UserRegistrateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    class Meta:
       model = User
       fields = ('email', 'password', 'password2')

    def create(self, validate_data):
        if validate_data['password']==validate_data['password2']:
            user_new=User.objects.create(
                email=validate_data['email'],
                password=make_password(validate_data['password'])
            )
            return user_new
        else:
            raise serializers.ValidationError("Пароли не совпадают")



class UserListSerializer(serializers.ModelSerializer):
    class Meta:
       model = User
       fields = "__all__"


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
       model = User    # модель джанго
       fields = ('description', 'age', 'gender', 'profile_image', 'first_name', 'last_name')

    def update(self, instance, validated_data):

        old_image = instance.profile_image

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.description = validated_data.get('description', instance.description)
        instance.age = validated_data.get('age', instance.age)
        instance.gender = validated_data.get('gender', instance.gender)


        if 'profile_image' in validated_data and validated_data['profile_image']:
            if old_image:
                if os.path.isfile(old_image.path):
                    os.remove(old_image.path)
            instance.profile_image = validated_data['profile_image']
        instance.save()
        return instance

