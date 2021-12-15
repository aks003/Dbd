from django.shortcuts import redirect, render
from schema.models import evaluation_db, rubrics_evaluation_db
from schema.models import student_db
<<<<<<< HEAD
from .forms import rubricsform
from schema.models import professor_db
from django import forms
=======
from . forms import rubrics_evaluation_dbform
from schema.models import professor_db,rubrics_evaluation_db

>>>>>>> 5cebe7579aa41478d383665bffe1511196d62e65

# Create your views here.
def details(request):
    if request.user.is_teacher:
        obj=professor_db.objects.get(email=request.user.email)
        obj1=student_db.objects.all().filter(prof_id=obj.prof_id)
        print(obj1)
    return render(request,'prof/prof_details.html',{'prof':obj,'stu':obj1})    
def marks(request):
    if request.user.is_teacher:
<<<<<<< HEAD
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

=======
        obj=professor_db.objects.get(email=request.user.email)
        obj1=student_db.objects.all().filter(prof_id=obj.prof_id)
        forms1=[]
        usn=[]
        i=0
        for a in obj1:
            fm=rubrics_evaluation_dbform()
            forms1.append(fm)
            u=a.usn
            usn.append(u)
        for a in forms1:
            print(a)    
        return render(request,'prof/marks.html',{'form':forms1,'usn':usn})
>>>>>>> 5cebe7579aa41478d383665bffe1511196d62e65
def stu_details(request):
    if request.user.is_teacher:
        return render(request,'prof/stu_details.html')