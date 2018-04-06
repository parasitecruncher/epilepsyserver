from django.contrib import admin

from models import Patient
from models import PatientSiezures

admin.site.register(PatientSiezures)
admin.site.register(Patient)
# Register your models here.
