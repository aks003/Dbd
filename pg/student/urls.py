from typing import Pattern
from django.urls import path
from . import views

urlpatterns=[
    path('',views.homepage,name="stu-home"),
    path('grade/',views.grade,name="grade"),
    path('deadlines/',views.deadline,name="dline"),
    
]

