from typing import Pattern
from django import urls
from django.urls import path
from django.urls.conf import include
from . import views

urlpatterns=[
    path('',views.home,name="home"),
    path('studentDetails',views.studentDetails,name="stuDetail"),
    path('professorDetails',views.professorDetails,name="profDetails"),
    path('marks',views.marks,name="marks"),
    path('marksInDetail',views.marksInDetail,name="marksInDetail"),
    path('autoComplete',views.autocomplete,name="autoComplete"),
    path('graph',views.graph,name="graph"),
    path('printPDF1',views.printPDF1,name="printPDF1"),
]

