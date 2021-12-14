from django.shortcuts import render
from schema.models import student_db

from schema.models import professor_db

# Create your views here.
def details(request):
    if request.user.is_teacher:
        obj=professor_db.objects.get(email=request.user.email)
        obj1=student_db.objects.all().filter(prof_id=obj.prof_id)
        print(obj1)
    return render(request,'prof/prof_details.html',{'prof':obj,'stu':obj1})    
def marks(request):
    if request.user.is_teacher:
        return render(request,'prof/marks.html')
def stu_details(request):
    if request.user.is_teacher:
        return render(request,'prof/stu_details.html')