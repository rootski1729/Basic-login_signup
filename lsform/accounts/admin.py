from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Blogcategory)
admin.site.register(Blogpost)
admin.site.register(Appointment)

