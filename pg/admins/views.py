from typing import Reversible
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from schema.models import phase_db, rubrics_db, student_db, professor_db, evaluation_db, rubrics_evaluation_db
from django.db.models import Q
from django.views.generic import View
from django.http import JsonResponse
import re
# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(Reversible("login"))
    elif request.user.is_student and request.user.is_teacher:
        return render(request, "dash.html", {"mail": request.user.email})
    else:
        return redirect("/home", {"mail": request.user.email})


def studentDetails(request):
    usn=''
    guide=''
    error=''
    flag=True
    if 'term' in request.GET:
        print('here')
        objects=student_db.objects.filter(usn__icontains=request.GET.get('term'))
        usn=[]
        for obj in objects:
            usn.append(obj.usn)
        return JsonResponse(usn,safe=False)
    if request.method == 'POST':
        usn=request.POST.get('usn')
        guide=request.POST.get('guide')
        if len(guide)!=0:
            regex_name = re.compile(r'^(Prof\.)\s*[A-Za-z\s*]{2,25}$', 
              re.IGNORECASE)
            res = regex_name.search(guide)
            if not res:
                flag=False
                error="Wrong input!"
        if len(usn)!=0:
            regex_name = re.compile(r'^(1RV)[0-9]{2}[A-Z]{3}[0-9]{2}$')
            res = regex_name.search(usn)
            if not res:
                flag=False
                error="Wrong input!"
   
    se_obj = []
    objects=student_db.objects.filter(branch="SE").order_by('usn')
    if flag and (len(usn)>0 or len(guide)>0):
        if len(usn)>0 and len(guide)==0:
            objects=student_db.objects.filter(branch="SE",usn=usn)
        elif len(usn)==0 and len(guide)>0: 
            objects=student_db.objects.filter(branch="SE",prof_id__name=guide)
        else:
            objects=student_db.objects.filter(branch="SE",usn=usn,prof_id__name=guide)
    for i in objects:
        se_obj.append(i)

    objects=student_db.objects.filter(branch="IT").order_by('usn')
    if flag and (len(usn)>0 or len(guide)>0):
        if len(usn)>0 and len(guide)==0:
            objects=student_db.objects.filter(branch="IT",usn=usn)
        elif len(usn)==0 and len(guide)>0: 
            objects=student_db.objects.filter(branch="IT",prof_id__name=guide)
        else:
            objects=student_db.objects.filter(branch="IT",usn=usn,prof_id__name=guide)
    it_obj = []
    for i in objects:
        it_obj.append(i)

    context = {"se_obj": se_obj,
    "it_obj":it_obj,
    "usn":usn,
    "guide":guide,
    "error":error,
    }
    return render(request, "stuDetails.html", context)


def professorDetails(request):
    prid=''
    name=''
    error=''
    flag=True

    if 'term' in request.GET:
        objects=professor_db.objects.filter(prof_id__icontains=request.GET.get('term'))
        prid=[]
        for obj in objects:
            prid.append(obj.prof_id)
        return JsonResponse(prid,safe=False)

    if request.method == 'POST':
        prid=request.POST.get('prid')
        name=request.POST.get('name')
        if len(name)!=0:
            regex_name = re.compile(r'^(Prof\.)\s*[A-Za-z\s*]{2,25}$', 
              re.IGNORECASE)
            res = regex_name.search(name)
            if not res:
                flag=False
                error="Wrong input!"
        if len(prid)!=0:
            regex_name = re.compile(r'^(IS)[0-9]{3}$')
            res = regex_name.search(prid)
            if not res:
                flag=False
                error="Wrong input!"
   
    d={}
    objects= professor_db.objects.all().order_by('prof_id')
    if flag and (len(prid)>0 or len(name)>0):
        if len(prid)>0 and len(name)==0:
            objects=professor_db.objects.filter(prof_id=prid)
        elif len(prid)==0 and len(name)>0: 
            objects=professor_db.objects.filter(name=name)
        else:
            objects=professor_db.objects.filter(prof_id=prid,name=name)
    for i in objects:
        names = []
        # print(student_db.objects.filter(prof_id=i.prof_id))
        t = list(student_db.objects.filter(prof_id=i.prof_id))
        print(t)
        temp = []
        for j in range(0, len(t)):
            tobj = t[j]
            temp.append(str(tobj.name) + "(" + tobj.branch + ")")
            names.extend(temp)
        d[i]=set(names)
    print(d)
    context = {
        "obj": d,
        "prof_id":prid,
        "name":name,
        "error":error
    }
    return render(request, "profDetails.html", context)

def marks(request):
    usn=''
    error=''
    flag=True
    if request.method == 'POST':
        usn=request.POST.get('usn')
        if len(usn)!=0:
            regex_name = re.compile(r'^(1RV)[0-9]{2}[A-Z]{3}[0-9]{2}$')
            res = regex_name.search(usn)
            if not res:
                flag=False
                error="Wrong input!"
    objects=student_db.objects.filter(branch='IT')
    if flag and (len(usn)>0):
        objects=student_db.objects.filter(branch='IT',usn=usn)
    it=[]
    for student in objects:
        eval_list=list(evaluation_db.objects.filter(usn=student.usn))
        marks=""
        if len(eval_list) == 0:
            it.append([student.usn,student.name,"-","-","Not generated"])
        for i in eval_list:
            marks=str(i.marks)
            it.append([student.usn,student.name,i.phase_id.category,i.phase_id.phase_number,marks])
    
    objects=student_db.objects.filter(branch='SE')
    if flag and (len(usn)>0):
        objects=student_db.objects.filter(branch='SE',usn=usn)
    se=[]
    for student in objects:
        eval_list=list(evaluation_db.objects.filter(usn=student.usn))
        marks=""
        if len(eval_list) == 0:
            se.append([student.usn,student.name,"-","-","Not generated"])
        for i in eval_list:
            marks=str(i.marks)
            se.append([student.usn,student.name,i.phase_id.category,i.phase_id.phase_number,marks])
    context={
        "it":it,
        "se":se,
        "usn":usn,
        "error":error
    }
    return render(request, "marks.html",context)

def marksInDetail(request):
    import re
    usn=''
    error=''
    flag=True
    if request.method == 'POST':
        usn=request.POST.get('usn')
        if len(usn)!=0:
            regex_name = re.compile(r'^(1RV)[0-9]{2}[A-Z]{3}[0-9]{2}$')
            res = regex_name.search(usn)
            if not res:
                flag=False
                error="Wrong input!"
    
    d={}
    it=[]
    it_panelist=[]
    profs=[]
    profd=[]
    #header
    objects=student_db.objects.filter(branch='IT').order_by('usn')
    if flag and (len(usn)>0):
        objects=student_db.objects.filter(branch='IT',usn=usn)

    for professor in professor_db.objects.filter(role='PANELIST-IT'):
        it_panelist.append(professor.name)
        profs.append(professor)
        profd.append(professor.name+"(PANELIST)")
    for student in objects:
        val=[]
        it=[]
        it.append(student.usn+" (Name:"+student.name+" Guide:"+student.prof_id.name+")")
        guide=list(professor_db.objects.filter(prof_id=student.prof_id))
        profs.append(*guide)
        for re in rubrics_evaluation_db.objects.filter(usn=student.usn).order_by('usn'):
            row=[]
            # print(re.rubrics.phase_id.category,re.rubrics.phase_id.phase_number,re.rubrics.rname,re.rubrics.r_max_marks)
            row.extend([re.rubrics.phase_id.category,re.rubrics.phase_id.phase_number,re.rubrics.rname,float(re.rubrics.r_max_marks)])
            trow=[]
            count=0
            for prof in profs: 
                tlist=list(rubrics_evaluation_db.objects.filter(usn=student.usn,prof_id=prof.prof_id,rubrics__rname=re.rubrics.rname,rubrics__phase_id=re.rubrics.phase_id))
                # print(tlist)
                if len(tlist) == 0:
                    trow.append('-')
                else:
                    trow.append(float(tlist[0].r_marks_obtained))
                    count+=1
            if count>0:
                row.extend(trow)
            else:
                row=[]
            if len(row)>0:
                val.append(row)
        it=tuple(it)
        d[it]=val   
        profs.remove(*guide)
    profd.append("GUIDE")

    e={}
    se=[]
    se_panelist=[]
    profs=[]
    prof_se=[]
    #header
    objects=student_db.objects.filter(branch='SE').order_by('usn')
    if flag and (len(usn)>0):
        objects=student_db.objects.filter(branch='SE',usn=usn)
    for professor in professor_db.objects.filter(role='PANELIST-SE'):
        se_panelist.append(professor.name)
        profs.append(professor)
        prof_se.append(professor.name+"(PANELIST)")
    for student in objects:
        val=[]
        se=[]
        se.append(student.usn+" (Name:"+student.name+" Guide:"+student.prof_id.name+")")
        guide=list(professor_db.objects.filter(prof_id=student.prof_id))
        profs.append(*guide)
        for re in rubrics_evaluation_db.objects.filter(usn=student.usn).order_by('usn'):
            row=[]
            # print(re.rubrics.phase_id.category,re.rubrics.phase_id.phase_number,re.rubrics.rname,re.rubrics.r_max_marks)
            row.extend([re.rubrics.phase_id.category,re.rubrics.phase_id.phase_number,re.rubrics.rname,float(re.rubrics.r_max_marks)])
            trow=[]
            count=0
            for prof in profs: 
                tlist=list(rubrics_evaluation_db.objects.filter(usn=student.usn,prof_id=prof.prof_id,rubrics__rname=re.rubrics.rname,rubrics__phase_id=re.rubrics.phase_id))
                # print(tlist)
                if len(tlist) == 0:
                    trow.append('-')
                else:
                    trow.append(float(tlist[0].r_marks_obtained))
                    count+=1
            if count>0:
                row.extend(trow)
            else:
                row=[]
            if len(row)>0:
                val.append(row)
        se=tuple(se)
        e[se]=val   
        profs.remove(*guide)
    
        #d[usn]
    # d={"name":["Akash","Vats"]}
    prof_se.append("GUIDE")
    context={
        "it_obj":d,
        "it_profs":profd,
        "se_obj":e,
        "se_profs":prof_se,
        "usn":usn,
        "error":error
    }
    return render(request, "marksInDetail.html",context)

def autocomplete(request):
    if 'term' in request.GET:
        objects=professor_db.objects.filter(name__icontains=request.GET.get('term'))
        name=[]
        for obj in objects:
            name.append(obj.name)
        return JsonResponse(name,safe=False)
    
def graph(request):
    select_value="Minor Project-1"
    if request.method == 'POST':
        select_value = request.POST.get('phase_id')
    l=[]
    for obj in evaluation_db.objects.filter(phase_id__category=select_value[:-2],phase_id__phase_number=select_value[-1]).order_by('usn'):
        l.append(obj)
    r=[]
    for obj in rubrics_db.objects.filter(phase_id__category=select_value[:-2],phase_id__phase_number=select_value[-1]):
        r.append(obj)
    p=[]
    for obj in phase_db.objects.filter():
        p.append(obj)
    return render(request,'charts.html',{"objs":l,"robjs":r,"pobjs":p,"disp":select_value})
