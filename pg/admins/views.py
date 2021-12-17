from typing import Reversible
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render

# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(Reversible("login"))
    elif request.user.is_student and request.user.is_teacher:
        return render(request,'dash.html',{'mail':request.user.email})
    else:
        return redirect('/home',{'mail':request.user.email})