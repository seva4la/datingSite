from rest_framework import serializers

from dating.models import User


class UserListSerializer(serializers.ModelSerializer):
   class Meta:
       model = User    # модель джанго
       fields = "__all__"

class UserUpdateDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['description']

