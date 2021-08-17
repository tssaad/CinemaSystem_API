"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.db import router
from django.urls import path
from django.urls.conf import include
from rest_framework import routers
from tickets import views

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('guests', views.ViewsetsGuest)
router.register('movies', views.ViewsetsMovie)
router.register('reservations', views.ViewsetsReservation)

urlpatterns = [
    path('admin/', admin.site.urls),
    #1
    path('django/test/', views.test),
    #2
    path('django/test2/', views.test2),
    #3.1
    path('rest/FBV/', views.FBV_list),
    #3.2
    path('rest/FBV/<int:pk>', views.FBV_pk),
    #4.1
    path('rest/CBV/', views.CBVList.as_view()),
    #4.2
    path('rest/CBV/<int:pk>', views.CBV_pk.as_view()),
    #5.1
    path('rest/mixins/', views.MixinsList.as_view()),
    #5.2
    path('rest/mixins/<int:pk>', views.Mixins_pk.as_view()),
    #6.1
    path('rest/generics/', views.GenericsList.as_view()),
    #6.2
    path('rest/generics/<int:pk>', views.Generics_pk.as_view()),
    #7
    path('rest/viewsets/', include(router.urls)),
    #8
    path('FBV/find_movies/', views.find_movie),
    #9
    path('FBV/reservations/', views.make_reservation),
]
