from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls.base import reverse
from django import forms
from schema.models import deliverables_db
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
    
    