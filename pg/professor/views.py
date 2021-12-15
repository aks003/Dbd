from django.shortcuts import render
from schema.models import student_db
from . forms import rubrics_evaluation_dbform
from schema.models import professor_db,rubrics_evaluation_db


# Create your views here.
def details(request):
    if request.user.is_teacher:
        obj=professor_db.objects.get(email=request.user.email)
        obj1=student_db.objects.all().filter(prof_id=obj.prof_id)
        print(obj1)
    return render(request,'prof/prof_details.html',{'prof':obj,'stu':obj1})    
def marks(request):
    if request.user.is_teacher:
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
def stu_details(request):
    if request.user.is_teacher:
        return render(request,'prof/stu_details.html')