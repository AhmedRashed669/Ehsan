from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(PatientCase_Donors)
# admin.site.register(GeneralDonations)

class DonorInline(admin.TabularInline):
    model = Donor.cases.through

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    inlines = [DonorInline]

@admin.register(GeneralDonations)
class GeneralDonation(admin.ModelAdmin):
    list_display = ('donor', 'amount', 'donation_date')