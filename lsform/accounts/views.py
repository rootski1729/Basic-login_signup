
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from .models import *
from .serializers import *
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import logout
from .forms import *
from google.oauth2 import service_account
from googleapiclient.discovery import build
from django.conf import settings
from django.urls import reverse
import os


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

@login_required(login_url='login')
def list_doctors(request):
    doctors = CustomUser.objects.filter(user_type='doctor')
    return render(request, 'accounts/list_doctors.html', {'doctors': doctors})

@login_required(login_url='login')
def get_booking_page(request, doctor_id):
    doctor = CustomUser.objects.get(id=doctor_id)
    if not doctor:
        messages.error(request, 'doctor not found')
        return redirect('list_doctors')
    return render(request, 'accounts/book_appointment.html', {'doctor': doctor})

@login_required(login_url='login')
def book_appointment(request,doctor_id):
    if request.method != 'POST':
        return redirect('list_doctors')
    patient = request.user
    speciality = request.POST.get('speciality')
    date= request.POST.get('date')
    start_time = request.POST.get('start_time')

    if not doctor_id or not speciality or not date or not start_time:
        return render(request, 'appointments/book_appointment.html', {'error': 'Missing required fields'})

    doctor=CustomUser.objects.get(id=doctor_id)
    if not doctor:
        messages.error(request, 'doctor not found')
        return redirect('list_doctors')
    
    
    date_obj = datetime.strptime(date, "%Y-%m-%d").date()
    start_time_obj= datetime.strptime(start_time, "%H:%M").time()
    
    startdatetime = datetime.combine(date_obj, start_time_obj)
    enddatetime = startdatetime + timedelta(minutes=45)
    end_time= enddatetime.time()
    
    if startdatetime < datetime.now():
        messages.error(request, 'You cannot book an appointment in the past')
        return redirect(reverse('book', kwargs={'doctor_id': doctor_id}))
    
    conflicts= Appointment.objects.filter(doctor=doctor, date=date_obj, start_time__lte=end_time, end_time__gte=start_time_obj)
    
    if conflicts:
        messages.error(request, 'you already have schedule for that time')
        return redirect(reverse('book', kwargs={'doctor_id': doctor_id}))


    appointment= Appointment.objects.create(
        patient=patient,
        doctor=doctor,
        speciality=speciality,
        date=date_obj,
        start_time=start_time_obj,  
        end_time=end_time
    )

    credentials = service_account.Credentials.from_service_account_file(
        settings.GOOGLE_CREDENTIALS_FILE,
        scopes=['https://www.googleapis.com/auth/calendar'])

    service= build('calendar', 'v3', credentials=credentials)
    event= {
        'summary': f'Appointment with {doctor.username}',
        'description': f'Appointment with {doctor.username} for {speciality}',
        'start': {'dateTime': startdatetime.isoformat(), 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': enddatetime.isoformat(), 'timeZone': 'Asia/Kolkata'},
    }

    service.events().insert(calendarId=os.getenv('calender_id'), body=event).execute()

    return redirect(reverse('appointment_success', kwargs={'appointment_id': appointment.id}))

def appointment_success(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    return render(request, 'accounts/appointment_success.html', {'appointment': appointment})

@login_required(login_url='login')
def get_appointments_patient(request):
    if request.user.user_type != 'patient':
        messages.error(request, 'Access denied')
        return redirect('login')
    
    user = request.user
    appointments = Appointment.objects.filter(patient=user)
    serializers= Appointmentserializer(appointments, many=True)
    return render(request, 'accounts/appointments.html', {'appointments': serializers.data})

@login_required(login_url='login')
def get_appointments_doctor(request):
    if request.user.user_type != 'doctor':
        messages.error(request, 'Access denied')
        return redirect('login')
    
    user = request.user
    appointments = Appointment.objects.filter(doctor=user)
    serializers= Appointmentserializer(appointments, many=True)
    return render(request, 'accounts/appointments.html', {'appointments': serializers.data})