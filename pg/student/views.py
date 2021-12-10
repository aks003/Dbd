from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse

# Create your views here.
def homepage(request):
    if request.user.is_student:
        return render(request,'student/dash.html')
    else:
        return HttpResponseRedirect(reverse("home"))

def grade(request):
    return render(request,'student/dash.html')

def deadline(request):
    return render(request,'student/dash.html')