
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import *
from .serializers import *
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import logout
from .forms import *
# Create your views here.

    
@csrf_protect
def Signup_view(request):
    if request.method == 'POST':
        form = signupform(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            messages.success(request, 'user created successfully')
            return redirect('login')
    else:
        form = signupform()
    return render(request, 'accounts/signup.html',{'form':form})      

@csrf_protect
def login_view(request):
    if request.method== 'POST':
        username=request.POST.get('username')
        password= request.POST.get('password')
        user = CustomUser.objects.filter(username=username)
        
        if user.exists():
            user = CustomUser.objects.get(username=username)
            if user.check_password(password):
                login(request, user)
                messages.success(request, f"welcome our customer {user.first_name}")
                if user.user_type == 'patient':
                    return redirect('patient_dashboard')
                elif user.user_type == 'doctor':
                    return redirect('doctor_dashboard')
            else:
                messages.error(request, "username or password incorrect")    
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

@login_required(login_url='login')
def create_blog_view(request):
    if request.user.user_type != 'doctor':
        messages.error(request, 'only doctor can create blog')
        return redirect('patient_dashboard')
    
    if request.method == 'POST':
        form = Blogpostform(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            messages.success(request, 'blog created successfully')
            return redirect('doctors_blog')
    else:
        form = Blogpostform()
    
    return render(request, 'accounts/create_blog.html',{'form':form})

@login_required(login_url='login')
def doctor_blogs_view(request):
    if request.user.user_type != 'doctor':
        messages.error(request, 'Access denied')
        return redirect('login')
    blogs = Blogpost.objects.filter(author=request.user)
    return render(request, 'accounts/doctor_blogs.html',{'blogs':blogs})

@login_required(login_url='login')
def patient_blogs_view(request):
    if request.user.user_type != 'patient':
        messages.error(request, 'Access denied')
        return redirect('login')
    
    categories = Blogcategory.objects.all()
    blogs_by_category = {category: Blogpost.objects.filter(category=category, status='published') for category in categories}

    return render(request, 'accounts/patient_blogs.html', {'blogs_by_category': blogs_by_category})