from django.shortcuts import redirect, render
from schema.models import evaluation_db, rubrics_evaluation_db
from schema.models import student_db
from .forms import rubricsform
from schema.models import professor_db
from django import forms

# Create your views here.
def details(request):
    if request.user.is_teacher:
        obj=professor_db.objects.get(email=request.user.email)
        obj1=student_db.objects.all().filter(prof_id=obj.prof_id)
        print(obj1)
    return render(request,'prof/prof_details.html',{'prof':obj,'stu':obj1})    
def marks(request):
    if request.user.is_teacher:
        if request.method == 'GET':
            obj=professor_db.objects.get(email=request.user.email)
            obj1=student_db.objects.all().filter(prof_id=obj.prof_id)
            obj2=evaluation_db.objects.all().filter(prof_id=obj.prof_id,)
            form1=[]
            usn1=[]
            for a in obj1:

                fm=rubricsform(initial={'usn':a.usn})
                fm.fields['usn'].widget=forms.HiddenInput()
                usn1.append(a.usn)
                form1.append(fm)
            list1=zip(form1,usn1)
            return render(request,'prof/marks.html',{'list':list1})
        else:
            form=rubricsform(request.POST)
            if form.is_valid():
                    form.save()
                    return redirect('details')

            else:
                return render(request,'student/deliverables.html',{'form':form})

def stu_details(request):
    if request.user.is_teacher:
        return render(request,'prof/stu_details.html')