from django.http import request
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from . forms import UserRegisterForm
from django.contrib import messages
import re
from django.contrib.auth import get_user_model

form = UserRegisterForm()

user = get_user_model()
# Create your views here.
# def login(request):
#     return render (request,'login.html')

def home(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        return render(request,'login/home.html',{'mail':request.user.email})

def signup(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        print("Reached here")
        str=request.POST['email']
        x = re.search('@rvce.edu.in$', str)
        y=False
        if len(str)<17 or x is False :
            print("invalid mail")
            messages.success(request, f'Wrong Mail')
        else:
            str1=str[-17:-12]
            y = bool(re.search("\.[a-z][a-z][0-2][0-9]", str1))
        if form.is_valid() and x  :
            print("REACHED INSIDE FORM IS VALID")
            user = form.save(commit=False)
            
            if y:
                user.is_student=True
                
            else:
                user.is_teacher=True

            user.save()    
            messages.success(request, f'Your account has been created ! You are now able to log in')
            return HttpResponseRedirect(reverse("home"))
    else:
        form = UserRegisterForm()
    return render(request,'login/login.html',{'form': form , 'rd':True})

def login_view(request):
    if request.method == 'POST':
        uname=request.POST['username']
        pwd=request.POST['password1']
        user= authenticate(request,username=uname,password=pwd)
        if user is not None:
            login(request, user)
            mail=user.email
            if user.is_student:
                return redirect('/student')
            else:
                return render(request,'login/home.html',{'mail':mail})
        else:
            return render(request,'login/login.html')
    form = UserRegisterForm()
    return render(request,'login/login.html',{'form':form,'rd':False})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


