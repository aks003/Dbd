from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django import forms
from schema.models import deliverables_db, evaluation_db, phase_db, rubrics_evaluation_db
from schema.models import professor_db
from schema.models import student_db
from .forms import DeliverablesForm
from django.contrib import messages

# Create your views here.
def homepage(request):
    if request.user.is_student:
        return render(request,'student/dash.html')
    else:
        return HttpResponseRedirect(reverse("home"))

def details(request):
    if request.user.is_student:
        student1=student_db.objects.get(email=request.user.email)
        prof=professor_db.objects.get(prof_id=student1.prof_id)
        print(prof)
        print(student1.prof_id)
        return render(request,'student/details.html',{'student':student1,'prof':prof})
    else:
        return HttpResponseRedirect(reverse("home"))

def deliverables(request):
    if request.user.is_student:
        mail1=request.user.email
        student1=student_db.objects.get(email=mail1).usn
        if request.method == 'GET':
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
            print('hi')
            print(request.POST['phase_id'])
            form = DeliverablesForm(request.POST)  
            obj = deliverables_db.objects.filter(usn=student1,phase_id=request.POST['phase_id']).first()
            print(obj)
            if obj: 
                obj.gdrive_link=request.POST['gdrive_link']
                obj.ppt=request.POST['ppt']
                obj.report=request.POST['report']
                obj.save()
                messages.success(request, f'Your have submitted the deliverables')
                return redirect('stu-home')
            else:
                # received_usn = student1
                # received_phase_id= request.POST.get('phase_id')
                # received_gdrive_link = request.POST.get('gdrive_link')
                # received_ppt = request.POST.get('ppt')
                # received_report = request.POST.get('report')
                # obj=deliverables_db()
                # obj.gdrive_link=request.POST['gdrive_link']
                # obj.ppt=request.POST['ppt']
                # obj.report=request.POST['report']
                # obj.usn=student1
                # obj.phase_id= request.POST.get('phase_id')
                # obj.save()
                print("3")
                if form.is_valid():
                    form.save()
                    print("4")
                    return redirect('home')

                else:
                    return render(request,'student/deliverables.html',{'form':form})
    else:
        return redirect("home")
    
def finalMarks(request):
    usn=student_db.objects.get(email=request.user.email)
    rubrics=rubrics_evaluation_db.objects.filter(usn=usn)
    guide=usn.prof_id
    role=professor_db.objects.get(prof_id=guide).role
    phase=""
    marks={}
    max_marks=0
    rolecheck="PANELIST-"+usn.branch
    for i in rubrics:
        s=i.rubrics
        s=str(s)
        # print(i.prof)
        max_marks+=float(s[-5:])
        ind=s.find('-')
        phase=s[:ind+2]
        marks_obtained=i.r_marks_obtained
        t2=0
        if "PANELIST" == rolecheck and i.prof == guide:
            marks_obtained*=2
            max_marks+=float(s[-5:])
            t2=1
        if marks.get(phase) is None:
            marks[phase]=[marks_obtained,1+t2]
        else:
            temp=marks.get(phase)
            marks[phase]=[temp[0]+marks_obtained,temp[1]+1+t2]
    if(len(rubrics)>0 and marks.get(phase)[1] == 12):
        print(marks.get(phase)[0],max_marks)
        ans=float(marks.get(phase)[0])/max_marks
        ans=float(ans)*100
        phase_obj=phase_db.objects.get(category=phase[:-2], phase_number=phase[-1])
        if evaluation_db.objects.filter(usn=usn,phase_id=phase_obj).first() is None:
            evaluation_db(usn=usn,prof_id=None,phase_id=phase_obj,marks=ans).save()
        context={'marks':ans,'phase':phase,'usn':usn}
        return render(request,'student/finalMarks.html',context)
    else:
        return render(request,'student/finalMarks.html',{'marks':0,'usn':usn})
    #guide is a panelist
    