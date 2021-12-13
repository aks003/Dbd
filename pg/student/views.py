from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls.base import reverse
from django import forms
from schema.models import professor_db
from schema.models import student_db
from .forms import DeliverablesForm

# Create your views here.
def homepage(request):
    if request.user.is_student:
        return render(request,'student/dash.html')
    else:
        return HttpResponseRedirect(reverse("home"))

def details(request):
    if request.user.is_student:
        student1=student_db.objects.get(email=request.user.email)
        prof=professor_db.objects.filter(prof_id=student1.prof_id).values('name')[0]
        print(prof)
        print(student1.prof_id)
        return render(request,'student/details.html',{'student':student1,'prof':prof})
    else:
        return HttpResponseRedirect(reverse("home"))

def deliverables(request):
    if request.user.is_student:
        if request.method == 'GET':
            mail1=request.user.email
            try:
                student1=student_db.objects.get(email=mail1).usn
                
            except :
                pass
            print(student1)
            form = DeliverablesForm(initial={'usn':student1,'phase_id':'1'})
            # form.fields['phase_id'].widget = forms.HiddenInput()
            form.fields['usn'].widget=forms.HiddenInput()
            return render(request,'student/deliverables.html', {'form': form , 'usn':student1 })
        else:
            form = DeliverablesForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse("home"))
                
            else:
                return render(request,'student/deliverables.html', {'form': form})
    else:
        return HttpResponseRedirect(reverse("home"))
    
    