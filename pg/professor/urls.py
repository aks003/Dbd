from typing import Pattern
from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns=[
    path('details/',views.details,name="details"),
    path('details/student',views.stu_details,name="stu_det"),
    path('marks/',views.marks,name="marks")
    
]
