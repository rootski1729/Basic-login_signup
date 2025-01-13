from django.urls import path
from .views import *

urlpatterns = [
    path('signup/',Signup_view,name='signup'),
    path('login/', login_view,name='login'),
    path('patient_dashboard/',patientdashboard_view, name='patient_dashboard'),
    path('doctor_dashboard/', doctordashboard_view,name='doctor_dashboard'),
]
