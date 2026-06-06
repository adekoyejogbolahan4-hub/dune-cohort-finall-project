from django.urls import path
from . import api_views

urlpatterns = [
    path('doctors/', api_views.DoctorListAPIView.as_view(), name='api_doctor_list'),
    path('doctors/<int:pk>/', api_views.DoctorDetailAPIView.as_view(), name='api_doctor_detail'),
    path('services/', api_views.ServiceListAPIView.as_view(), name='api_service_list'),
    path('appointments/', api_views.AppointmentListCreateAPIView.as_view(), name='api_appointment_list_create'),
    path('appointments/<int:pk>/', api_views.AppointmentDeleteAPIView.as_view(), name='api_appointment_delete'),
]
