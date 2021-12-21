from django.shortcuts import redirect, render
from schema.models import deliverables_db
from schema.models import rubrics_db
from schema.models import evaluation_db, rubrics_evaluation_db
from schema.models import student_db
from .forms import rubricsform
from schema.models import professor_db
from django import forms

# Create your views here.
def details(request):
    if request.user.is_teacher :
        obj=professor_db.objects.get(email=request.user.email)
        obj1=student_db.objects.all().filter(prof_id=obj.prof_id)
        return render(request,'prof/prof_details.html',{'prof':obj,'stu':obj1})    
def marks(request):
    if request.user.is_teacher:
        if request.method == 'GET':
            usn=request.GET.get('mark')
            prof=professor_db.objects.get(email=request.user.email)
            prof_id=prof.prof_id
            students=student_db.objects.all().filter(prof_id=prof_id)
            rubrics= rubrics_db.objects.all()
            phase=rubrics.first().phase_id
            rubrics_eval=rubrics_evaluation_db.objects.all().filter(usn=usn)
            print(rubrics_eval)
            deliverables=deliverables_db.objects.all().filter(usn=usn,phase_id=phase)
            print(deliverables)
            return render(request,'prof/marks1.html',{
                'prof':prof,
                'usn':usn,
                'rubrics':rubrics,
                'rubrics_eval':rubrics_eval,
                'len':len(rubrics_eval),
                'phase':phase,
                'deli':deliverables,
                })
            
        else:
            for a in rubrics_db.objects.all():
                marks=request.POST[a.rname]
                usn=request.POST['usn']
                student=student_db.objects.filter(usn=usn).first()
                professor=professor_db.objects.get(email=request.user.email)
                rubrics_eval=rubrics_evaluation_db(usn=student,prof=professor,rubrics=a,r_marks_obtained=marks)
                rubrics_eval.save()
                students=student_db.objects.all().filter(prof_id=rubrics_eval.prof_id)
            return render(request,'prof/prof_details.html',{'prof':professor,'stu':students})  

def stu_details(request):
    if request.user.is_teacher:
        return render(request,'prof/stu_details.html')