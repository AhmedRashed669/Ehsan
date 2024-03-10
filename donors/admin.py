from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(PatientCase_Donors)

class DonorInline(admin.TabularInline):
    model = Donor.cases.through

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    inlines = [DonorInline]