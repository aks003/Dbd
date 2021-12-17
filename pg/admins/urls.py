from typing import Pattern
from django import urls
from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns=[
    path('',views.home,name="home"),
]

