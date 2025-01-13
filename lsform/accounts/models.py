from django.db import models
from django.contrib.auth.models import AbstractUser

type_user = (
    ('patient', 'Patient'),
    ('doctor', 'Doctor'),
)
class CustomUser(AbstractUser):
    user_type = models.CharField(choices=type_user, max_length=10)
    profile_pic = models.ImageField(upload_to='profile_pic/', null=True, blank=True)
    address_line1 = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=255, null= True, blank = True)
    pincode = models.CharField(max_length=10,blank=True, null=True)
    
    def __str__(self):
        return self.username
    