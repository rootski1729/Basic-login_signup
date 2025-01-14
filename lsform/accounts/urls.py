from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('signup/',Signup_view,name='signup'),
    path('login/', login_view,name='login'),
    path('logout/', logout_view, name='logout'), 
    path('patient_dashboard/',patientdashboard_view, name='patient_dashboard'),
    path('doctor_dashboard/', doctordashboard_view,name='doctor_dashboard'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)