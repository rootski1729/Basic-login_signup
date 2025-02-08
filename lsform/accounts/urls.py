from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/login/', permanent=False)),
    path('signup/',Signup_view,name='signup'),
    path('login/', login_view,name='login'),
    path('logout/', logout_view, name='logout'), 
    path('patient_dashboard/',patientdashboard_view, name='patient_dashboard'),
    path('doctor_dashboard/', doctordashboard_view,name='doctor_dashboard'),
    path('create_blog/', create_blog_view,name='create_blog'),
    path('doctors_blog/', doctor_blogs_view,name='doctors_blog'),
    path('patient_blog/', patient_blogs_view,name='patient_blog'),
    path('doctors/', list_doctors,name='doctors'),
    path('book/<int:doctor_id>/', get_booking_page,name='book'),
    path('book-appointment/<int:doctor_id>/', book_appointment,name='book_appointment'),
    path('appointment_success/<int:appointment_id>/', appointment_success,name='appointment_success'),
    path('doctor_appointments/', get_appointments_doctor,name='doctor_appointments'),
    path('patient_appointments/', get_appointments_patient,name='patient_appointments'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
