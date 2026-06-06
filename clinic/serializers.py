from rest_framework import serializers
from .models import Doctor, Service, Specialisation
from appointments.models import Appointment


class SpecialisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialisation
        fields = ['id', 'name', 'description']


class DoctorSerializer(serializers.ModelSerializer):
    specialisation_name = serializers.CharField(source='specialisation.name', read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id', 'first_name', 'last_name', 'specialisation', 'specialisation_name',
            'email', 'phone', 'bio', 'is_available', 'years_experience'
        ]


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'price', 'duration_minutes', 'is_active']


class AppointmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.full_name', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)
    patient_username = serializers.CharField(source='patient.username', read_only=True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'patient', 'patient_username', 'doctor', 'doctor_name',
            'service', 'service_name', 'appointment_date', 'appointment_time',
            'status', 'notes', 'created_at'
        ]
        read_only_fields = ['patient', 'created_at']
