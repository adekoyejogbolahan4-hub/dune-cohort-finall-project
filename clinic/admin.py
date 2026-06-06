from django.contrib import admin
from .models import Specialisation, Doctor, Service


@admin.register(Specialisation)
class SpecialisationAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'specialisation', 'email', 'is_available', 'years_experience')
    list_filter = ('specialisation', 'is_available')
    search_fields = ('first_name', 'last_name', 'email')
    list_editable = ('is_available',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration_minutes', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    list_editable = ('is_active',)
