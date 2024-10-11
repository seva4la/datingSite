"""
URL configuration for siteDating project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from xml.etree.ElementInclude import include

from django.contrib import admin
from django.urls import path, include
from dating.urls import *
from dating.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dating/', include('dating.urls')),
    path('api/v1/UserList/', UserApiListView.as_view()),
    path('api/v1/UserUpdateDescription/<uuid:pk>', UserApiUpdateDescription.as_view()),
    path('api/v1/UserDelete/<uuid:pk>', UserApiDelete.as_view()),
    path('api/v1/UserRetrieve/<uuid:pk>', UserApiRetriveView.as_view()),
    path('api/v1/UserCreate/', UserApiCreate.as_view()),
]
