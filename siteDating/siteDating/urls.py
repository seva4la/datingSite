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
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dating/', include('dating.urls')),
    path('api/v1/UserList/', UserApiListView.as_view()),           # список данных всех пользователей
    path('api/v1/UserDelete/<uuid:pk>', UserApiDelete.as_view()),  # удаление пользователя по id
    path('api/v1/UserRetrieve/<uuid:pk>', UserApiRetriveView.as_view()), #получение всех данных пользователя по id
    path('api/v1/UserUpdate/<uuid:pk>/', UserUpdate.as_view()),    # редактирование имени/возраста/пола/фотографии/описания
    path('api/v1/UserRegistration/', UserApiRegistrate.as_view()), # регистрация по почте и паролю
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
