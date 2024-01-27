from django.contrib import admin
from .models import Hospital,HospitalEmployee,SystemEmployee
# Register your models here.
admin.site.register(Hospital)
admin.site.register(HospitalEmployee)
admin.site.register(SystemEmployee)
