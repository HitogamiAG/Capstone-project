"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from home import views as views_home
from messenger import views as views_messenger

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views_home.home),
    path('', views_home.home, name='home-home'),
    path('messenger/', views_messenger.messenger, name='messenger-home'),
    path('<str:room>/', views_messenger.room, name='messenger-room'),
    path('messenger/checkview', views_messenger.checkview, name='checkview'),
    path('send', views_messenger.send, name='messenger-send'),
    path('getMessages/<str:room>/', views_messenger.getMessages, name='messenger-getMessages'),
]
