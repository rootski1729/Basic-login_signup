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
    
blogcategory = [('covid19','covid19'),('Mental health','Mental health'),('fitness','fitness'),('food','food'),('lifestyle','lifestyle')]
class Blogcategory(models.Model):
    name = models.CharField(max_length=255,unique=True,choices=blogcategory)
    
    def __str__(self):
        return self.name
    
class Blogpost(models.Model):
    DRAFT = 'draft'
    PUBLISHED= 'published'
    STATUS = [
        (DRAFT, 'draft'),
        (PUBLISHED, 'published'),
    ]
    
    title = models.CharField(max_length=255)
    image= models.ImageField(upload_to='blog_image/',blank=True,null=True)
    category = models.ForeignKey(Blogcategory, on_delete=models.CASCADE,related_name='category')
    summary = models.TextField(max_length=300)
    content= models.TextField()
    status= models.CharField(max_length=10,choices=STATUS,default=DRAFT)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name='author')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title