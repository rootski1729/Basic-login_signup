
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import CustomUser
from .serializers import *
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import logout
# Create your views here.

    
@csrf_protect
def Signup_view(request):
    if request.method == 'POST':
        form = signupform(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                return redirect('login')
            except Exception as e:
                return render(request, 'accounts/signup.html', {'form': form, 'errors': "something went wrong"})
        else:
            return render(request, 'accounts/signup.html', {'form': form, 'errors': form.errors})
    return render(request, 'accounts/signup.html', {'form': signupform()})


@csrf_protect
def login_view(request):
    if request.method== 'POST':
        username=request.POST.get('username')
        password= request.POST.get('password')
        user = CustomUser.objects.filter(username=username, password=password)
        if user.exists():
            user = CustomUser.objects.get(username=username, password=password)
            login(request, user)
            messages.success(request, f"welcome our customer {user.first_name}")
            if user.user_type == 'patient':
                return redirect('patient_dashboard')
            elif user.user_type == 'doctor':
                return redirect('doctor_dashboard')
            
        else:
            messages.error(request, "username or password incorrect") 
    return render(request, 'accounts/login.html')




def logout_view(request):
    logout(request)
    messages.success(request, 'logged out successfully')
    return redirect('login')  


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
