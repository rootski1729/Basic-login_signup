
from django.shortcuts import render,redirect
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import CustomUser
from .serializers import *
from rest_framework import status
from django.contrib.auth import authenticate, login
# Create your views here.

@csrf_protect
def Signup_view(request):
    if request.method == 'POST':
        serializer= signupserializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return redirect('login')
        else:
            return render(request, 'accounts/signup.html', {'serializer': serializer, 'errors': serializer.errors})
    return render(request, 'accounts/signup.html')

@csrf_protect
def login_view(request):
    if request.method== 'POST':
        username=request.POST.get('username')
        password= request.POST.get('password')
        
        user = authenticate(request,username=username, password=password)
        if hasattr(user, 'user_type'):
            login(request, user)
            if user.user_type == 'patient':
                return redirect('patient_dashboard')
            
            elif user.user_type=='doctor':
                return redirect('doctor_dashboard')
            
        return render(request, 'accounts/login.html', {'error':'Invalid credentials'})
    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def patientdashboard_view(request):
    if getattr(request.user, 'user_type') != 'patient':
        return redirect('login')
    
    return render(request, 'accounts/patient_dashboard.html',{'user':request.user})
    
            
@login_required(login_url='login')
def doctordashboard_view(request):
    if getattr(request.user, 'user_type') != 'doctor':
        return redirect('login')
    return render(request, 'accounts/doctor_dashboard.html',{'user':request.user})