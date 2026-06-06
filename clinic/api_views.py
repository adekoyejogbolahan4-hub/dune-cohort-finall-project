from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Doctor, Service
from appointments.models import Appointment
from .serializers import DoctorSerializer, ServiceSerializer, AppointmentSerializer


class DoctorListAPIView(generics.ListAPIView):
    """GET /api/doctors/ — List all available doctors."""
    queryset = Doctor.objects.filter(is_available=True).select_related('specialisation')
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class DoctorDetailAPIView(generics.RetrieveAPIView):
    """GET /api/doctors/<pk>/ — Retrieve a single doctor."""
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ServiceListAPIView(generics.ListAPIView):
    """GET /api/services/ — List all active services."""
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class AppointmentListCreateAPIView(generics.ListCreateAPIView):
    """
    GET  /api/appointments/ — List the authenticated user's appointments.
    POST /api/appointments/ — Book a new appointment (auth required).
    """
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Appointment.objects.filter(
            patient=self.request.user
        ).select_related('doctor', 'service')

    def perform_create(self, serializer):
        serializer.save(patient=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentDeleteAPIView(APIView):
    """DELETE /api/appointments/<pk>/ — Cancel an appointment (auth required)."""
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk, patient=request.user)
        appointment.delete()
        return Response({'message': 'Appointment cancelled.'}, status=status.HTTP_204_NO_CONTENT)
