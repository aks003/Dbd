from django.shortcuts import redirect, render
from schema.models import rubrics_db
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
        obj2=rubrics_db.objects.all()
        usn=0
        obj=professor_db.objects.get(email=request.user.email)
        prof=obj.prof_id
        obj1=student_db.objects.all().filter(prof_id=obj.prof_id)
        obj2= rubrics_db.objects.all()
        if request.method == 'GET':
            usn=request.GET.get('mark')
            obj=professor_db.objects.get(email=request.user.email)
            prof=obj.prof_id
            obj1=student_db.objects.all().filter(prof_id=obj.prof_id)
            obj2= rubrics_db.objects.all()
            # obj=professor_db.objects.get(email=request.user.email)
            # obj1=student_db.objects.all().filter(prof_id=obj.prof_id)
            # obj2=evaluation_db.objects.all().filter(prof_id=obj.prof_id,)
            # form1=[]
            # usn1=[]
            # prof=obj.prof_id
            # for a in obj1:

            #     fm=rubricsform(initial={'usn':a.usn})
            #     fm.fields['usn'].widget=forms.HiddenInput()
            #     fm.fields['prof'].widget=forms.HiddenInput()
            #     usn1.append(a.usn)
            #     form1.append(fm)
            # list1=zip(form1,usn1)
        
            return render(request,'prof/marks1.html',{'prof':prof,'usn':usn,'obj2':obj2})
            print(usn)
        else:
            for a in obj2:
                marks=request.POST[a.rname]
                usn1=request.POST['usn']
                obj2=student_db.objects.filter(usn=usn1).first()
                obj3=professor_db.objects.get(email=request.user.email)
                print(usn1)
                obj=rubrics_evaluation_db(usn=obj2,prof=obj3,rubrics=a,r_marks_obtained=marks)
                obj.save()
                obj1=student_db.objects.all().filter(prof_id=obj.prof_id)
            return render(request,'prof/prof_details.html',{'prof':obj3,'stu':obj1})  

def stu_details(request):
    if request.user.is_teacher:
        return render(request,'prof/stu_details.html')