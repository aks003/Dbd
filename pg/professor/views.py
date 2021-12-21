from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from schema.models import deliverables_db
from schema.models import rubrics_db
from schema.models import evaluation_db, rubrics_evaluation_db
from schema.models import student_db
from .forms import rubricsform
from schema.models import professor_db
from django import forms
from django.urls import reverse
# Create your views here.
def details(request):
    if request.user.is_teacher :
        obj=professor_db.objects.get(email=request.user.email)
        obj1=student_db.objects.all().filter(prof_id=obj.prof_id)
        role=obj.role.upper()
        return render(request,'prof/prof_details.html',{'prof':obj,'stu':obj1,'role':role})    
def marks(request):
    if request.user.is_teacher:
        professor=professor_db.objects.get(email=request.user.email)
        if request.method == 'GET':
            usn=request.GET.get('mark')
            prof=professor_db.objects.get(email=request.user.email)
            prof_id=prof.prof_id
            students=student_db.objects.all().filter(prof_id=prof_id)
            rubrics= rubrics_db.objects.all()
            phase=rubrics.first().phase_id
            rubrics_eval=rubrics_evaluation_db.objects.all().filter(usn=usn,prof_id=prof_id)
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
            role=professor.role.upper()
            return render(request,'prof/prof_details.html',{'prof':professor,'stu':students,'role':role})  

def stu_details(request):
    if request.user.is_teacher:
        return render(request,'prof/stu_details.html')

def panelist(request):
    professor=professor_db.objects.get(email=request.user.email)
    role=professor.role.upper()
    if request.user.is_teacher and (role == "PANELIST-IT" or role == "PANELIST-SE"):
        i=role.find('-')
        branch=role[i+1:]
        if(branch == "IT"):
            students=student_db.objects.filter(branch="IT")
            print(students)
            return render(request,'prof/panelist-base.html',{'prof':professor,'stu':students,'branch':branch})
        if(branch == "SE"):
            students=student_db.objects.filter(branch="SE")
            print(students)
            return render(request,'prof/panelist-base.html',{'prof':professor,'stu':students,'branch':branch})
    else:
        return render(request,'prof.no_access.html')

def panelistEntry(request):
    try:
        professor=professor_db.objects.get(email=request.user.email)
        role=professor.role.upper()
        if request.user.is_teacher and role == "PANELIST-IT":
            i=role.find('-')
            branch=role[i+1:]
            if(branch == "IT"):
                if request.method == 'GET':
                    usn=request.GET.get('mark')
                    prof_id=professor.prof_id
                    students=student_db.objects.filter(branch="IT")
                    rubrics= rubrics_db.objects.all()
                    phase=rubrics.first().phase_id
                    rubrics_eval=rubrics_evaluation_db.objects.all().filter(usn=usn,prof_id=prof_id)
                    length=len(rubrics_eval)
                    return render(request,'prof/panelist-marks.html',{
                        'prof':professor,
                        'usn':usn,
                        'rubrics':rubrics,
                        'rubrics_eval':rubrics_eval,
                        'len':length,
                        'phase':phase
                        })
                else:
                    for a in rubrics_db.objects.all():
                        marks=request.POST[a.rname]
                        usn=request.POST['usn']
                        student=student_db.objects.filter(usn=usn).first()
                        professor=professor_db.objects.get(email=request.user.email)
                        rubrics_eval=rubrics_evaluation_db(usn=student,prof=professor,rubrics=a,r_marks_obtained=marks)
                        rubrics_eval.save()
                        students=student_db.objects.filter(branch="IT")
                    role=professor.role.upper()
                    return HttpResponseRedirect(reverse('panelist'))
        if request.user.is_teacher and role == "PANELIST-SE":
            i=role.find('-')
            branch=role[i+1:]
            if(branch == "SE"):
                if request.method == 'GET':
                    usn=request.GET.get('mark')
                    prof_id=professor.prof_id
                    students=student_db.objects.filter(branch="SE")
                    rubrics= rubrics_db.objects.all()
                    phase=rubrics.first().phase_id
                    rubrics_eval=rubrics_evaluation_db.objects.all().filter(usn=usn,prof_id=prof_id)
                    length=len(rubrics_eval)
                    return render(request,'prof/panelist-marks.html',{
                        'prof':professor,
                        'usn':usn,
                        'rubrics':rubrics,
                        'rubrics_eval':rubrics_eval,
                        'len':length,
                        'phase':phase
                        })
                else:
                    for a in rubrics_db.objects.all():
                        marks=request.POST[a.rname]
                        usn=request.POST['usn']
                        student=student_db.objects.filter(usn=usn).first()
                        professor=professor_db.objects.get(email=request.user.email)
                        rubrics_eval=rubrics_evaluation_db(usn=student,prof=professor,rubrics=a,r_marks_obtained=marks)
                        rubrics_eval.save()
                        students=student_db.objects.filter(branch="SE")
                    role=professor.role.upper()  
                    return HttpResponseRedirect(reverse('panelist'))
                    # return render(request,'prof/panelist-base.html',{'prof':professor,'stu':students,'role':role})        
        else:
            return render(request,'prof/no_access.html')
    except:
        return render(request,'prof/no_access.html')