from typing import Pattern
from django.urls import path
from . import views

urlpatterns=[
    path('',views.homepage,name="stu-home"),
    path('details/',views.details,name="grade"),
    path('deliverables/',views.deliverables,name="dline"),
    path('final-marks/',views.finalMarks,name='finalMarks')
    
]

