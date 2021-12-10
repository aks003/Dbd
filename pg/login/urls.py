from typing import Pattern
from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns=[
    path('',views.home,name="home"),
    path('login/',views.login_view,name="login"),
    path('logout/',views.logout_view,name="logout"),
    path('signup/',views.signup,name="signup"),
    path('student/',include('student.urls'))
]

